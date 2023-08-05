from logging import getLogger
import time
from clickzetta.client import Client
from clickzetta.bulkload.bulkload_enums import BulkLoadMetaData, BulkLoadCommitOptions, BulkLoadState, \
    BulkLoadCommitMode
from clickzetta.bulkload.bulkload_writer import BulkLoadWriter

_logger = getLogger(__name__)


class BulkLoadStream:
    def __init__(self, meta_data: BulkLoadMetaData, client: Client):
        self.meta_data = meta_data
        self.client = client

    def get_stream_id(self):
        return self.meta_data.get_stream_id()

    def get_operation(self):
        return self.meta_data.get_operation()

    def get_stream_state(self):
        return self.meta_data.get_state()

    def get_sql_error(self):
        return self.meta_data.get_sql_error_msg()

    def get_schema(self):
        return self.meta_data.get_schema_name()

    def get_table(self):
        return self.meta_data.get_table()

    def get_record_keys(self):
        return self.meta_data.get_record_keys()

    def get_partition_specs(self):
        return self.meta_data.get_partition_specs()

    def open_writer(self, partition_id: int):
        config = self.client.open_bulkload_stream_writer(self.meta_data.get_instance_id(),
                                                         self.meta_data.get_workspace(),
                                                         self.meta_data.get_schema_name(),
                                                         self.meta_data.get_table_name(),
                                                         self.meta_data.get_stream_id(), partition_id)

        return BulkLoadWriter(self.client, self.meta_data, config, partition_id)

    def commit(self, options: BulkLoadCommitOptions):
        _logger.info("Committing BulkLoadStream:" + self.meta_data.get_stream_id())
        self.client.commit_bulkload_stream(self.meta_data.get_instance_id(), self.meta_data.get_workspace(),
                                           self.meta_data.get_schema_name(), self.meta_data.get_table_name(),
                                           self.meta_data.get_stream_id(), options.workspace, options.vc,
                                           BulkLoadCommitMode.COMMIT_STREAM)
        if not options.async_commit:
            state = BulkLoadState.COMMIT_SUBMITTED
            sql_error_msg = ''
            for try_time in range(options.poll_times):
                current_stream = BulkLoadStream(self.client.get_bulkload_stream(self.meta_data.get_schema_name(),
                                                                                self.meta_data.get_table_name(),
                                                                                self.meta_data.get_stream_id()),
                                                self.client)
                state = current_stream.get_stream_state()
                sql_error_msg = current_stream.get_sql_error()
                _logger.info(
                    "Get BulkLoadStream:" + self.meta_data.get_stream_id() + ", state:" + state + ",time:" + try_time)
                if state == BulkLoadState.COMMIT_SUCCESS or state == BulkLoadState.COMMIT_FAILED:
                    break
                else:
                    time.sleep(options.poll_interval_ms / 1000)
            if state != BulkLoadState.COMMIT_SUCCESS:
                raise IOError(
                    "BulkLoadStream:" + self.get_stream_id() + " sync commit failed or timeout with state:" + state
                    + " with error:" + sql_error_msg)

    def abort(self):
        _logger.info("Aborting BulkLoadStream:" + self.meta_data.get_stream_id())
        ret = self.client.commit_bulkload_stream(self.meta_data.get_instance_id(), self.meta_data.get_workspace(),
                                                 self.meta_data.get_schema_name(), self.meta_data.get_table_name(),
                                                 self.meta_data.get_stream_id(), '', '',
                                                 BulkLoadCommitMode.ABORT_STREAM)
        if ret.get_state() != BulkLoadState.ABORTED:
            raise IOError(
                "BulkLoadStream:" + self.get_stream_id() + " abort failed ")

    def close(self):
        return
