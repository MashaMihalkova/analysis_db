from sqlalchemy import Column, Integer, DateTime, Text, Boolean, Float, BigInteger, PrimaryKeyConstraint

from common.helpers import decorator
from db.models.common import Base


@decorator("_asdict")
class Project(Base):
    __tablename__ = "project"
    id_wbs = Column(Integer, nullable=True, index=False, unique=True)
    id_project = Column(Integer, primary_key=True, index=True, unique=True)
    project_code = Column(Text, nullable=True, index=False)
    project_name = Column(Text, nullable=True, index=False)
    project_date = Column(DateTime, nullable=True, index=False)
    sum_base_proj_id = Column(Integer, nullable=True, index=False)
    last_publication = Column(DateTime, nullable=True, index=False)
    business_unit = Column(Text, nullable=False, index=True, unique=False)


@decorator("_asdict")
class ProjectPMC(Base):
    __tablename__ = "project_pmc"

    id_wbs = Column(Integer, nullable=True, index=False, unique=True)
    id_project = Column(Integer, primary_key=True, index=True, unique=True)
    project_code = Column(Text, nullable=True, index=False)
    project_name = Column(Text, nullable=True, index=False)
    project_date = Column(DateTime, nullable=True, index=False)
    sum_base_proj_id = Column(Integer, nullable=True, index=False)
    last_publication = Column(DateTime, nullable=True, index=False)
    business_unit = Column(Text, nullable=False, index=True, unique=False)


@decorator("_asdict")
class ProjectDel(Base):
    __tablename__ = "project_del"

    id_project = Column(Integer, primary_key=True, index=True, unique=True)


@decorator("_asdict")
class ISR(Base):
    __tablename__ = "ISR"

    id_ISR = Column(Integer, primary_key=True, index=True, unique=True)
    parent_id_ISR = Column(Integer, nullable=True, index=False)
    id_wbs = Column(Integer, nullable=True, index=False)
    id_project = Column(Integer, nullable=True, index=False)
    isr_code = Column(Text, nullable=True, index=False)
    isr_name = Column(Text, nullable=True, index=False)
    update_date = Column(DateTime, nullable=False, index=False)
    business_unit = Column(Text, nullable=False, index=True)


@decorator("_asdict")
class ISRPMC(Base):
    __tablename__ = "ISR_pmc"

    id_ISR = Column(Integer, primary_key=True, index=True, unique=True)
    parent_id_ISR = Column(Integer, nullable=True, index=False)
    id_wbs = Column(Integer, nullable=True, index=False)
    id_project = Column(Integer, nullable=True, index=False)
    isr_code = Column(Text, nullable=True, index=False)
    isr_name = Column(Text, nullable=True, index=False)
    update_date = Column(DateTime, nullable=False, index=False)
    business_unit = Column(Text, nullable=False, index=True)


@decorator("_asdict")
class ISRDel(Base):
    __tablename__ = "ISR_del"

    id_ISR = Column(Integer, primary_key=True, index=True, unique=True)


@decorator("_asdict")
class Activity(Base):
    __tablename__ = "activity"

    id_activity = Column(Integer, primary_key=True, index=True, unique=True)
    id_wbs = Column(Integer, nullable=True, index=False)
    id_project = Column(Integer, nullable=True, index=False)
    id_isr = Column(Integer, nullable=True, index=False)
    activity_code = Column(Text, nullable=True, index=False)
    activity_name = Column(Text, nullable=True, index=False)
    total_float_hr_cnt = Column(Float, nullable=True, index=False)
    status_code = Column(Text, nullable=True, index=False)
    IsCtritical = Column(Boolean, nullable=True, index=False)
    PlannedStartDate = Column(DateTime, nullable=True, index=False)
    PlannedFinishDate = Column(DateTime, nullable=True, index=False)
    ActualStartDate = Column(DateTime, nullable=True, index=False)
    ActualFinishDate = Column(DateTime, nullable=True, index=False)
    StartDate = Column(DateTime, nullable=True, index=False)
    FinishDate = Column(DateTime, nullable=True, index=False)
    BaselineStartDate = Column(DateTime, nullable=True, index=False)
    BaselineFinishDate = Column(DateTime, nullable=True, index=False)
    update_date = Column(DateTime, nullable=False, index=False)
    business_unit = Column(Text, nullable=False, index=True)
    activity_type = Column(Text, nullable=True, index=False)


@decorator("_asdict")
class ActivityPMC(Base):
    __tablename__ = "activity_pmc"

    id_activity = Column(Integer, primary_key=True, index=True, unique=True)
    id_wbs = Column(Integer, nullable=True, index=False)
    id_project = Column(Integer, nullable=True, index=False)
    id_isr = Column(Integer, nullable=True, index=False)
    activity_code = Column(Text, nullable=True, index=False)
    activity_name = Column(Text, nullable=True, index=False)
    total_float_hr_cnt = Column(Float, nullable=True, index=False)
    status_code = Column(Text, nullable=True, index=False)
    IsCtritical = Column(Boolean, nullable=True, index=False)
    PlannedStartDate = Column(DateTime, nullable=True, index=False)
    PlannedFinishDate = Column(DateTime, nullable=True, index=False)
    ActualStartDate = Column(DateTime, nullable=True, index=False)
    ActualFinishDate = Column(DateTime, nullable=True, index=False)
    StartDate = Column(DateTime, nullable=True, index=False)
    FinishDate = Column(DateTime, nullable=True, index=False)
    BaselineStartDate = Column(DateTime, nullable=True, index=False)
    BaselineFinishDate = Column(DateTime, nullable=True, index=False)
    update_date = Column(DateTime, nullable=False, index=False)
    business_unit = Column(Text, nullable=False, index=True)
    activity_type = Column(Text, nullable=True, index=False)


@decorator("_asdict")
class ActivityDel(Base):
    __tablename__ = "activity_del"

    id_activity = Column(Integer, primary_key=True, index=True, unique=True)


@decorator("_asdict")
class Resource(Base):
    __tablename__ = "resource"

    id_resource = Column(Integer, primary_key=True, index=True)
    parent_id_resource = Column(Integer, nullable=True, index=False)
    resource_code = Column(Text, nullable=True, index=False)
    resource_name = Column(Text, nullable=True, index=False)
    resource_type = Column(Text, nullable=True, index=False)
    unit_name = Column(Text, nullable=True, index=False)
    update_date = Column(DateTime, nullable=False, index=False)
    business_unit = Column(Text, nullable=False, index=True)


@decorator("_asdict")
class ResourcePMC(Base):
    __tablename__ = "resource_pmc"

    id_resource = Column(Integer, primary_key=True, index=True)
    parent_id_resource = Column(Integer, nullable=True, index=False)
    resource_code = Column(Text, nullable=True, index=False)
    resource_name = Column(Text, nullable=True, index=False)
    resource_type = Column(Text, nullable=True, index=False)
    unit_name = Column(Text, nullable=True, index=False)
    update_date = Column(DateTime, nullable=False, index=False)
    business_unit = Column(Text, nullable=False, index=True)


@decorator("_asdict")
class ResourceDel(Base):
    __tablename__ = "resource_del"

    id_resource = Column(Integer, primary_key=True, index=True, unique=True)


@decorator("_asdict")
class Resassignment(Base):
    __tablename__ = "resassignment"

    id_resassignment = Column(Integer, primary_key=True, index=True, unique=True)
    id_activity = Column(Integer, nullable=True, index=False)
    id_resource = Column(Integer, nullable=True, index=False)
    id_wbs = Column(Integer, nullable=True, index=False)
    id_project = Column(Integer, nullable=True, index=False)
    target_qty = Column(Float, nullable=True, index=False)
    remain_qty = Column(Float, nullable=True, index=False)
    act_reg_qty = Column(Float, nullable=True, index=False)
    resource_type = Column(Text, nullable=True, index=False)
    update_date = Column(DateTime, nullable=False, index=False)
    business_unit = Column(Text, nullable=False, index=True)


@decorator("_asdict")
class ResassignmentPMC(Base):
    __tablename__ = "resassignment_pmc"

    id_resassignment = Column(Integer, primary_key=True, index=True, unique=True)
    id_activity = Column(Integer, nullable=True, index=False)
    id_resource = Column(Integer, nullable=True, index=False)
    id_wbs = Column(Integer, nullable=True, index=False)
    id_project = Column(Integer, nullable=True, index=False)
    target_qty = Column(Float, nullable=True, index=False)
    remain_qty = Column(Float, nullable=True, index=False)
    act_reg_qty = Column(Float, nullable=True, index=False)
    resource_type = Column(Text, nullable=True, index=False)
    update_date = Column(DateTime, nullable=False, index=False)
    business_unit = Column(Text, nullable=False, index=True)


@decorator("_asdict")
class ResassignmentDel(Base):
    __tablename__ = "resassignment_del"

    id_resassignment = Column(Integer, primary_key=True, index=True, unique=True)


@decorator("_asdict")
class UDFCodeProject(Base):
    __tablename__ = "udf_code_project"

    id_wbs = Column(Integer, nullable=True, index=False)
    id_project = Column(Integer, primary_key=True, index=True, unique=True)
    update_date = Column(DateTime, nullable=False, index=False)
    business_unit = Column(Text, nullable=False, index=True)
    ShowOnPortal_code = Column(Text, nullable=True, index=False)
    ShowOnPortal_name = Column(Text, nullable=True, index=False)
    ShowOnPortal_id = Column(Integer, nullable=True, index=False)
    WriteOnPortal_code = Column(Text, nullable=True, index=False)
    WriteOnPortal_name = Column(Text, nullable=True, index=False)
    WriteOnPortal_id = Column(Integer, nullable=True, index=False)
    Portf_code = Column(Text, nullable=True, index=False)
    Portf_name = Column(Text, nullable=True, index=False)
    Portf_id = Column(Integer, nullable=True, index=False)
    udf_flag_text = Column(Text, nullable=True, index=False)
    udf_flag_number = Column(Float, nullable=True, index=False)
    udf_flag_date = Column(DateTime, nullable=True, index=False)
    svod_report_code = Column(Text, nullable=True, index=False)
    svod_report_name = Column(Text, nullable=True, index=False)
    svod_report_id = Column(Integer, nullable=True, index=False)


@decorator("_asdict")
class UDFCodeProjectPMC(Base):
    __tablename__ = "udf_code_project_pmc"

    id_wbs = Column(Integer, nullable=True, index=False)
    id_project = Column(Integer, primary_key=True, index=True, unique=True)
    update_date = Column(DateTime, nullable=False, index=False)
    business_unit = Column(Text, nullable=False, index=True)
    ShowOnPortal_code = Column(Text, nullable=True, index=False)
    ShowOnPortal_name = Column(Text, nullable=True, index=False)
    ShowOnPortal_id = Column(Integer, nullable=True, index=False)
    WriteOnPortal_code = Column(Text, nullable=True, index=False)
    WriteOnPortal_name = Column(Text, nullable=True, index=False)
    WriteOnPortal_id = Column(Integer, nullable=True, index=False)
    Portf_code = Column(Text, nullable=True, index=False)
    Portf_name = Column(Text, nullable=True, index=False)
    Portf_id = Column(Integer, nullable=True, index=False)
    udf_flag_text = Column(Text, nullable=True, index=False)
    udf_flag_number = Column(Float, nullable=True, index=False)
    udf_flag_date = Column(DateTime, nullable=True, index=False)
    svod_report_code = Column(Text, nullable=True, index=False)
    svod_report_name = Column(Text, nullable=True, index=False)
    svod_report_id = Column(Integer, nullable=True, index=False)


@decorator("_asdict")
class UDFCodeProjectDel(Base):
    __tablename__ = "udf_code_project_del"

    id_project = Column(Integer, primary_key=True, index=True, unique=True)


@decorator("_asdict")
class UDFCodeActivity(Base):
    __tablename__ = "udf_code_activity"

    id_activity = Column(Integer, primary_key=True, index=True, unique=True)
    id_wbs = Column(Integer, nullable=True, index=False)
    id_project = Column(Integer, nullable=True, index=False)
    update_date = Column(DateTime, nullable=False, index=False)
    business_unit = Column(Text, nullable=False, index=True)
    constr_code = Column(Text, nullable=True, index=False)
    constr_name = Column(Text, nullable=True, index=False)
    constr_id = Column(Integer, nullable=True, index=False)
    work_type_code = Column(Text, nullable=True, index=False)
    work_type_name = Column(Text, nullable=True, index=False)
    work_type_id = Column(Integer, nullable=True, index=False)
    stage_code = Column(Text, nullable=True, index=False)
    stage_name = Column(Text, nullable=True, index=False)
    stage_id = Column(Integer, nullable=True, index=False)
    contractor_code = Column(Text, nullable=True, index=False)
    contractor_name = Column(Text, nullable=True, index=False)
    contractor_id = Column(Integer, nullable=True, index=False)
    mto_code = Column(Text, nullable=True, index=False)
    mto_name = Column(Text, nullable=True, index=False)
    mto_id = Column(Integer, nullable=True, index=False)
    stage_ms_code = Column(Text, nullable=True, index=False)
    stage_ms_name = Column(Text, nullable=True, index=False)
    stage_ms_id = Column(Integer, nullable=True, index=False)
    realisation_stage_code = Column(Text, nullable=True, index=False)
    realisation_stage_name = Column(Text, nullable=True, index=False)
    realisation_stage_id = Column(Integer, nullable=True, index=False)
    fo_plan_text = Column(Text, nullable=True, index=False)
    fo_plan_number = Column(Float, nullable=True, index=False)
    fo_plan_date = Column(Integer, nullable=True, index=False)
    fo_fact_text = Column(Text, nullable=True, index=False)
    fo_fact_number = Column(Float, nullable=True, index=False)
    fo_fact_date = Column(Integer, nullable=True, index=False)
    fo_remaining_text = Column(Text, nullable=True, index=False)
    fo_remaining_number = Column(Float, nullable=True, index=False)
    fo_remaining_date = Column(DateTime, nullable=True, index=False)
    uom_text = Column(Text, nullable=True, index=False)
    uom_number = Column(Float, nullable=True, index=False)
    uom_date = Column(DateTime, nullable=True, index=False)
    note_text = Column(Text, nullable=True, index=False)
    note_number = Column(Float, nullable=True, index=False)
    note_date = Column(DateTime, nullable=True, index=False)
    shifr_rd_text = Column(Text, nullable=True, index=False)
    shifr_rd_number = Column(Float, nullable=True, index=False)
    shifr_rd_date = Column(DateTime, nullable=True, index=False)
    subcontractor_code = Column(Text, nullable=True, index=False)
    subcontractor_name = Column(Text, nullable=True, index=False)
    subcontractor_id = Column(Integer, nullable=True, index=False)


@decorator("_asdict")
class UDFCodeActivityPMC(Base):
    __tablename__ = "udf_code_activity_pmc"

    id_activity = Column(Integer, primary_key=True, index=True, unique=True)
    id_wbs = Column(Integer, nullable=True, index=False)
    id_project = Column(Integer, nullable=True, index=False)
    update_date = Column(DateTime, nullable=False, index=False)
    business_unit = Column(Text, nullable=False, index=True)
    constr_code = Column(Text, nullable=True, index=False)
    constr_name = Column(Text, nullable=True, index=False)
    constr_id = Column(Integer, nullable=True, index=False)
    work_type_code = Column(Text, nullable=True, index=False)
    work_type_name = Column(Text, nullable=True, index=False)
    work_type_id = Column(Integer, nullable=True, index=False)
    stage_code = Column(Text, nullable=True, index=False)
    stage_name = Column(Text, nullable=True, index=False)
    stage_id = Column(Integer, nullable=True, index=False)
    contractor_code = Column(Text, nullable=True, index=False)
    contractor_name = Column(Text, nullable=True, index=False)
    contractor_id = Column(Integer, nullable=True, index=False)
    mto_code = Column(Text, nullable=True, index=False)
    mto_name = Column(Text, nullable=True, index=False)
    mto_id = Column(Integer, nullable=True, index=False)
    stage_ms_code = Column(Text, nullable=True, index=False)
    stage_ms_name = Column(Text, nullable=True, index=False)
    stage_ms_id = Column(Integer, nullable=True, index=False)
    realisation_stage_code = Column(Text, nullable=True, index=False)
    realisation_stage_name = Column(Text, nullable=True, index=False)
    realisation_stage_id = Column(Integer, nullable=True, index=False)
    fo_plan_text = Column(Text, nullable=True, index=False)
    fo_plan_number = Column(Float, nullable=True, index=False)
    fo_plan_date = Column(Integer, nullable=True, index=False)
    fo_fact_text = Column(Text, nullable=True, index=False)
    fo_fact_number = Column(Float, nullable=True, index=False)
    fo_fact_date = Column(Integer, nullable=True, index=False)
    fo_remaining_text = Column(Text, nullable=True, index=False)
    fo_remaining_number = Column(Float, nullable=True, index=False)
    fo_remaining_date = Column(DateTime, nullable=True, index=False)
    uom_text = Column(Text, nullable=True, index=False)
    uom_number = Column(Float, nullable=True, index=False)
    uom_date = Column(DateTime, nullable=True, index=False)
    note_text = Column(Text, nullable=True, index=False)
    note_number = Column(Float, nullable=True, index=False)
    note_date = Column(DateTime, nullable=True, index=False)
    shifr_rd_text = Column(Text, nullable=True, index=False)
    shifr_rd_number = Column(Float, nullable=True, index=False)
    shifr_rd_date = Column(DateTime, nullable=True, index=False)
    subcontractor_code = Column(Text, nullable=True, index=False)
    subcontractor_name = Column(Text, nullable=True, index=False)
    subcontractor_id = Column(Integer, nullable=True, index=False)


@decorator("_asdict")
class UDFCodeActivityDel(Base):
    __tablename__ = "udf_code_activity_del"

    id_activity = Column(Integer, primary_key=True, index=True, unique=True)


@decorator("_asdict")
class DictionaryActivityCode(Base):
    __tablename__ = "dictionary_activity_code"

    id = Column(Integer, primary_key=True, index=True)
    Dictionary_Name = Column(Text, nullable=True, index=False)
    id_parent = Column(Integer, nullable=True, index=False)
    code = Column(Text, nullable=True, index=False)
    name = Column(Text, nullable=True, index=False)
    full_code = Column(Text, nullable=True, index=False)
    id_wbs = Column(Integer, nullable=True, index=False)
    id_project = Column(Integer, nullable=True, index=False)
    update_date = Column(DateTime, nullable=True, index=False)
    business_unit = Column(Text, nullable=False, index=True)


@decorator("_asdict")
class DictionaryActivityCodePMC(Base):
    __tablename__ = "dictionary_activity_code_pmc"

    id = Column(Integer, primary_key=True, index=True)
    Dictionary_Name = Column(Text, nullable=True, index=False)
    id_parent = Column(Integer, nullable=True, index=False)
    code = Column(Text, nullable=True, index=False)
    name = Column(Text, nullable=True, index=False)
    full_code = Column(Text, nullable=True, index=False)
    id_wbs = Column(Integer, nullable=True, index=False)
    id_project = Column(Integer, nullable=True, index=False)
    update_date = Column(DateTime, nullable=True, index=False)
    business_unit = Column(Text, nullable=False, index=True)


@decorator("_asdict")
class DictionaryActivityCodeDel(Base):
    __tablename__ = "dictionary_activity_code_del"

    id = Column(Integer, primary_key=True, index=True, unique=True)


@decorator("_asdict")
class DictionaryProjectCode(Base):
    __tablename__ = "dictionary_project_code"

    id = Column(Integer, primary_key=True, index=True)
    Dictionary_Name = Column(Text, nullable=True, index=False)
    id_parent = Column(Integer, nullable=True, index=False)
    code = Column(Text, nullable=True, index=False)
    name = Column(Text, nullable=True, index=False)
    full_code = Column(Text, nullable=True, index=False)
    update_date = Column(DateTime, nullable=True, index=False)
    business_unit = Column(Text, nullable=False, index=True)


@decorator("_asdict")
class DictionaryProjectCodePMC(Base):
    __tablename__ = "dictionary_project_code_pmc"

    id = Column(Integer, primary_key=True, index=True)
    Dictionary_Name = Column(Text, nullable=True, index=False)
    id_parent = Column(Integer, nullable=True, index=False)
    code = Column(Text, nullable=True, index=False)
    name = Column(Text, nullable=True, index=False)
    full_code = Column(Text, nullable=True, index=False)
    update_date = Column(DateTime, nullable=True, index=False)
    business_unit = Column(Text, nullable=False, index=True)


@decorator("_asdict")
class DictionaryProjectCodeDel(Base):
    __tablename__ = "dictionary_project_code_del"

    id = Column(Integer, primary_key=True, index=True, unique=True)


@decorator("_asdict")
class DictionaryResourceCode(Base):
    __tablename__ = "dictionary_resource_code"

    id = Column(Integer, primary_key=True, index=True)
    Dictionary_Name = Column(Text, nullable=True, index=False)
    id_parent = Column(Integer, nullable=True, index=False)
    code = Column(Text, nullable=True, index=False)
    name = Column(Text, nullable=True, index=False)
    full_code = Column(Text, nullable=True, index=False)
    update_date = Column(DateTime, nullable=True, index=False)
    business_unit = Column(Text, nullable=False, index=True)


@decorator("_asdict")
class DictionaryResourceCodePMC(Base):
    __tablename__ = "dictionary_resource_code_pmc"

    id = Column(Integer, primary_key=True, index=True)
    Dictionary_Name = Column(Text, nullable=True, index=False)
    id_parent = Column(Integer, nullable=True, index=False)
    code = Column(Text, nullable=True, index=False)
    name = Column(Text, nullable=True, index=False)
    full_code = Column(Text, nullable=True, index=False)
    update_date = Column(DateTime, nullable=True, index=False)
    business_unit = Column(Text, nullable=False, index=True)


@decorator("_asdict")
class DictionaryResourceCodeDel(Base):
    __tablename__ = "dictionary_resource_code_del"

    id = Column(Integer, primary_key=True, index=True, unique=True)


class UDFCodeResource(Base):
    __tablename__ = "udf_code_resource"

    id_resource = Column(Integer, primary_key=True, index=True)
    update_date = Column(DateTime, nullable=False, index=False)
    business_unit = Column(Text, nullable=False, index=True)
    stg_code = Column(Text, nullable=True, index=False)
    stg_name = Column(Text, nullable=True, index=False)
    stg_id = Column(Integer, nullable=True, index=False)
    accounting_code = Column(Text, nullable=True, index=False)
    accounting_name = Column(Text, nullable=True, index=False)
    accounting_id = Column(Integer, nullable=True, index=False)
    is_fo_code = Column(Text, nullable=True, index=False)
    is_fo_name = Column(Text, nullable=True, index=False)
    is_fo_id = Column(Integer, nullable=True, index=False)
    traffic_light_code = Column(Text, nullable=True, index=False)
    traffic_light_name = Column(Text, nullable=True, index=False)
    traffic_light_id = Column(Integer, nullable=True, index=False)
    stg_type_code = Column(Text, nullable=True, index=False)
    stg_type_name = Column(Text, nullable=True, index=False)
    stg_type_id = Column(Integer, nullable=True, index=False)
    specialty_code = Column(Text, nullable=True, index=False)
    specialty_name = Column(Text, nullable=True, index=False)
    specialty_id = Column(Integer, nullable=True, index=False)


class UDFCodeResourcePMC(Base):
    __tablename__ = "udf_code_resource_pmc"

    id_resource = Column(Integer, primary_key=True, index=True)
    update_date = Column(DateTime, nullable=False, index=False)
    business_unit = Column(Text, nullable=False, index=True)
    stg_code = Column(Text, nullable=True, index=False)
    stg_name = Column(Text, nullable=True, index=False)
    stg_id = Column(Integer, nullable=True, index=False)
    accounting_code = Column(Text, nullable=True, index=False)
    accounting_name = Column(Text, nullable=True, index=False)
    accounting_id = Column(Integer, nullable=True, index=False)
    is_fo_code = Column(Text, nullable=True, index=False)
    is_fo_name = Column(Text, nullable=True, index=False)
    is_fo_id = Column(Integer, nullable=True, index=False)
    traffic_light_code = Column(Text, nullable=True, index=False)
    traffic_light_name = Column(Text, nullable=True, index=False)
    traffic_light_id = Column(Integer, nullable=True, index=False)
    stg_type_code = Column(Text, nullable=True, index=False)
    stg_type_name = Column(Text, nullable=True, index=False)
    stg_type_id = Column(Integer, nullable=True, index=False)
    specialty_code = Column(Text, nullable=True, index=False)
    specialty_name = Column(Text, nullable=True, index=False)
    specialty_id = Column(Integer, nullable=True, index=False)


@decorator("_asdict")
class UDFCodeResourceDel(Base):
    __tablename__ = "udf_code_resource_del"

    id_resource = Column(Integer, primary_key=True, index=True)


@decorator("_asdict")
class UDFCodeResassignment(Base):
    __tablename__ = "udf_code_resassignment"

    id_resassignment = Column(Integer, primary_key=True, index=True)
    id_wbs = Column(Integer, nullable=True, index=False)
    id_project = Column(Integer, nullable=True, index=False)
    update_date = Column(DateTime, nullable=False, index=False)
    business_unit = Column(Text, nullable=False, index=True)
    change_coef_text = Column(Text, nullable=True, index=False)
    change_coef_number = Column(Float, nullable=True, index=False)
    change_coef_date = Column(DateTime, nullable=True, index=False)


@decorator("_asdict")
class UDFCodeResassignmentPMC(Base):
    __tablename__ = "udf_code_resassignment_pmc"

    id_resassignment = Column(Integer, primary_key=True, index=True)
    id_wbs = Column(Integer, nullable=True, index=False)
    id_project = Column(Integer, nullable=True, index=False)
    update_date = Column(DateTime, nullable=False, index=False)
    business_unit = Column(Text, nullable=False, index=True)
    change_coef_text = Column(Text, nullable=True, index=False)
    change_coef_number = Column(Float, nullable=True, index=False)
    change_coef_date = Column(DateTime, nullable=True, index=False)


@decorator("_asdict")
class UDFCodeResassignmentDel(Base):
    __tablename__ = "udf_code_resassignment_del"

    id_resassignment = Column(Integer, primary_key=True, index=True)


@decorator("_asdict")
class ActvRel(Base):
    __tablename__ = "actvrel"

    id_actvrel = Column(Integer, primary_key=True, index=True)
    id_wbs = Column(Integer, nullable=True, index=False)
    id_project = Column(Integer, nullable=True, index=False)
    id_activity = Column(Integer, nullable=True, index=False)
    pred_id_activity = Column(Integer, nullable=True, index=False)
    pred_type = Column(Text, nullable=True, index=False)
    lag_hr_cnt = Column(Float, nullable=True, index=False)
    update_date = Column(DateTime, nullable=False, index=False)
    business_unit = Column(Text, nullable=False, index=False)


@decorator("_asdict")
class ActvRelPMC(Base):
    __tablename__ = "actvrel_pmc"

    id_actvrel = Column(Integer, primary_key=True, index=True)
    id_wbs = Column(Integer, nullable=True, index=False)
    id_project = Column(Integer, nullable=True, index=False)
    id_activity = Column(Integer, nullable=True, index=False)
    pred_id_activity = Column(Integer, nullable=True, index=False)
    pred_type = Column(Text, nullable=True, index=False)
    lag_hr_cnt = Column(Float, nullable=True, index=False)
    update_date = Column(DateTime, nullable=False, index=False)
    business_unit = Column(Text, nullable=False, index=False)


@decorator("_asdict")
class ActvRelDel(Base):
    __tablename__ = "actvrel_del"

    id_actvrel = Column(Integer, primary_key=True, index=True)


@decorator("_asdict")
class ResassignmentSpred(Base):
    __tablename__ = "resassignmentspred"

    id_resassignment = Column(Integer)
    id_activity = Column(Integer, nullable=True, index=False)
    id_resource = Column(Integer, nullable=True, index=False)
    id_wbs = Column(Integer, nullable=True, index=False)
    id_project = Column(Integer, nullable=True, index=False)
    dt = Column(DateTime)
    target_qty = Column(Float, nullable=True, index=False)
    remain_qty = Column(Float, nullable=True, index=False)
    act_reg_qty = Column(Float, nullable=True, index=False)
    business_unit = Column(Text, nullable=False, index=True)
    update_date = Column(DateTime, nullable=True, index=False)
    id = Column(BigInteger, nullable=True, index=False)

    table_args = (
        PrimaryKeyConstraint(id_resassignment, dt),
        {},
    )


@decorator("_asdict")
class ResassignmentSpredPMC(Base):
    __tablename__ = "resassignmentspred_pmc"

    id_resassignment = Column(Integer)
    id_activity = Column(Integer, nullable=True, index=False)
    id_resource = Column(Integer, nullable=True, index=False)
    id_wbs = Column(Integer, nullable=True, index=False)
    id_project = Column(Integer, nullable=True, index=False)
    dt = Column(DateTime)
    target_qty = Column(Float, nullable=True, index=False)
    remain_qty = Column(Float, nullable=True, index=False)
    act_reg_qty = Column(Float, nullable=True, index=False)
    business_unit = Column(Text, nullable=False, index=True)
    update_date = Column(DateTime, nullable=True, index=False)
    id = Column(BigInteger, nullable=True, index=False)

    table_args = (
        PrimaryKeyConstraint(id_resassignment, dt),
        {},
    )


@decorator("_asdict")
class ResassignmentSpredDel(Base):
    __tablename__ = "resassignmentspred_del"

    id_resassignment = Column(Integer)
    dt = Column(DateTime)

    table_args = (
        PrimaryKeyConstraint(id_resassignment, dt),
        {},
    )
