from pretty_pie_log import PieLogger, PieLogLevel

Logger = PieLogger(
    logger_name="main",
    minimum_log_level=PieLogLevel.DEBUG,
    log_file_size_limit=int(100 * 1024 * 1024),
    timestamp_padding=25,
    log_level_padding=10,
    max_backup_files=10,
)
