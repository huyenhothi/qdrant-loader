from __future__ import annotations

import os
import threading
from typing import Any

from qdrant_loader.utils.logging import LoggingConfig


async def run_pipeline_ingestion(
    settings: Any,
    qdrant_manager: Any,
    *,
    project: str | None,
    source_type: str | None,
    source: str | None,
    force: bool,
    metrics_dir: str | None = None,
) -> None:
    from qdrant_loader.core.async_ingestion_pipeline import AsyncIngestionPipeline
    logger = LoggingConfig.get_logger(__name__)

    # import tracemalloc
    # tracemalloc.start()

    pipeline = (
        AsyncIngestionPipeline(settings, qdrant_manager, metrics_dir=metrics_dir)
        if metrics_dir
        else AsyncIngestionPipeline(settings, qdrant_manager)
    )

    print(
        f"PIPELINE CREATED 1  | pid={os.getpid()} | pipeline_obj_id={id(pipeline)}"
    )
    print("PID:", os.getpid())
    print("Current thread:", threading.current_thread().name)
    print("Active threads:", threading.active_count())
    for j in threading.enumerate():
        print(" -", j.name)

    ingestion_error: Exception | None = None
    try:
        # print("Truoc process")
        await pipeline.process_documents(
            project_id=project,
            source_type=source_type,
            source=source,
            force=force,
        )
        print(
            f"PIPELINE CREATED 2  | pid={os.getpid()} | pipeline_obj_id={id(pipeline)}"
        )
        print("PID:", os.getpid())
        print("Current thread:", threading.current_thread().name)
        print("Active threads:", threading.active_count())
        for i in threading.enumerate():
            print(" -", i.name)
        
        # print("Snapshot lan 1")
        # snapshot = tracemalloc.take_snapshot()
        # top_stats = snapshot.statistics("lineno")

        # for stat in top_stats[:10]:
        #     print(stat)

    except Exception as e:
        ingestion_error = e
        # Record full stack trace for ingestion failures
        logger.exception("Ingestion failed")
    cleanup_error: Exception | None = None

    # tracemalloc.start()

    try:
        # print("Chuan bị clean up")
        await pipeline.cleanup()
        # print("Sau khi clean up")
    except Exception as e:
        cleanup_error = e
        if ingestion_error is not None:
            # If ingestion already failed, annotate that cleanup also failed
            logger.exception("Cleanup failed after ingestion exception")
        else:
            logger.exception("Cleanup failed after successful ingestion")
    if ingestion_error is not None:
        raise ingestion_error
    if cleanup_error is not None:
        raise cleanup_error
    
    # print("Snapshot lan 2")
    # snapshot_2 = tracemalloc.take_snapshot()
    # top_stats_2 = snapshot_2.statistics("lineno")

    # for stat in top_stats_2[:10]:
    #     print(stat)
    print(
        f"PIPELINE CREATED 3  | pid={os.getpid()} | pipeline_obj_id={id(pipeline)}"
    )
    print("PID:", os.getpid())
    print("Current thread:", threading.current_thread().name)
    print("Active threads:", threading.active_count())
    for i in threading.enumerate():
        print(" -", i.name)
