from flask import request

from app.common.model import WorkflowSchema, WorkflowMetricsSchema, InstanceSchema
from app.common.database import database


@database
def get_report(report_id=None, database=None):
    report_dao = database.report_dao()
    report = report_dao.get(report_id=report_id)

    if report_id is not None and not report:
        return {
            "message": f"Report {report_id} doesn't exist"
        }, 404

    return ReportSchema(many=(report_id is None)).dump(report)

