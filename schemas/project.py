from datetime import datetime
from pydantic import BaseModel, validator
from typing import Optional, List


class Project(BaseModel):
    id_wbs: Optional[int]
    id_project: int
    project_code: str
    project_name: str
    project_date: Optional[datetime]
    sum_base_proj_id: Optional[int]
    last_publication: Optional[datetime]
    business_unit: Optional[str]

    def to_db_update_model(self):
        source_dict = super().dict(
            by_alias=True, exclude={"project_code", "last_publication", "business_unit"}
        )

        return source_dict

    def to_db_insert_model(self):
        source_dict = super().dict(by_alias=True, exclude={"last_publication"})

        return source_dict


class ISR(BaseModel):
    id_ISR: int
    parent_id_ISR: Optional[int]
    id_wbs: Optional[int]
    id_project: Optional[int]
    isr_code: Optional[str]
    isr_name: Optional[str]
    update_date: Optional[datetime]
    business_unit: Optional[str]

    def to_db_update_model(self):
        source_dict = super().dict(by_alias=True, exclude={"id_ISR", "business_unit"})

        return source_dict

    def to_db_insert_model(self):
        source_dict = super().dict(by_alias=True, exclude={})

        return source_dict


class Activity(BaseModel):
    id_activity: int
    id_wbs: Optional[int]
    id_project: Optional[int]
    id_isr: Optional[int]
    activity_code: Optional[str]
    activity_name: Optional[str]
    total_float_hr_cnt: Optional[float]
    status_code: Optional[str]
    IsCtritical: Optional[bool]
    PlannedStartDate: Optional[datetime]
    PlannedFinishDate: Optional[datetime]
    ActualStartDate: Optional[datetime]
    ActualFinishDate: Optional[datetime]
    StartDate: Optional[datetime]
    FinishDate: Optional[datetime]
    BaselineStartDate: Optional[datetime]
    BaselineFinishDate: Optional[datetime]
    update_date: Optional[datetime]
    business_unit: Optional[str]
    activity_type: Optional[str]

    def to_db_update_model(self):
        source_dict = super().dict(
            by_alias=True, exclude={"id_activity", "business_unit"}
        )

        return source_dict

    def to_db_insert_model(self):
        source_dict = super().dict(by_alias=True, exclude={})

        return source_dict


class Resource(BaseModel):
    id_resource: int
    parent_id_resource: Optional[int]
    resource_code: Optional[str]
    resource_name: Optional[str]
    resource_type: Optional[str]
    unit_name: Optional[str]
    update_date: Optional[datetime]
    business_unit: Optional[str]

    def to_db_update_model(self):
        source_dict = super().dict(
            by_alias=True, exclude={"id_resource", "business_unit"}
        )

        return source_dict

    def to_db_insert_model(self):
        source_dict = super().dict(by_alias=True, exclude={})

        return source_dict


class Resassignment(BaseModel):
    id_resassignment: int
    id_activity: Optional[int]
    id_resource: Optional[int]
    id_wbs: Optional[int]
    id_project: Optional[int]
    target_qty: Optional[float]
    remain_qty: Optional[float]
    act_reg_qty: Optional[float]
    resource_type: Optional[str]
    update_date: Optional[datetime]
    business_unit: Optional[str]

    def to_db_update_model(self):
        source_dict = super().dict(
            by_alias=True, exclude={"id_resassignment", "business_unit"}
        )

        return source_dict

    def to_db_insert_model(self):
        source_dict = super().dict(by_alias=True, exclude={})

        return source_dict


class UDFCodeSettings(BaseModel):
    id_udf_code_settings: int
    dictionary_type_internal_code: Optional[str]
    dictionary_name: Optional[str]
    column_name_prefix: Optional[str]


class UDFCodeProject(BaseModel):
    id_wbs: Optional[int]
    id_project: int
    update_date: Optional[datetime]
    business_unit: Optional[str]
    ShowOnPortal_code: Optional[str]
    ShowOnPortal_name: Optional[str]
    ShowOnPortal_id: Optional[int]
    WriteOnPortal_code: Optional[str]
    WriteOnPortal_name: Optional[str]
    WriteOnPortal_id: Optional[int]
    Portf_code: Optional[str]
    Portf_name: Optional[str]
    Portf_id: Optional[int]
    udf_flag_text: Optional[str]
    udf_flag_number: Optional[float]
    udf_flag_date: Optional[datetime]
    svod_report_code: Optional[str]
    svod_report_name: Optional[str]
    svod_report_id: Optional[int]

    def to_db_update_model(self):
        source_dict = super().dict(
            by_alias=True, exclude={"id_project", "business_unit"}
        )

        return source_dict

    def to_db_insert_model(self):
        source_dict = super().dict(by_alias=True, exclude={})

        return source_dict


class TableValidationInfo(BaseModel):
    fixed_columns_len: int
    dynamic_columns_mul_by: int
    dictionary_type_internal_codes: List[str]


class UDFCodeActivity(BaseModel):
    id_activity: int
    id_wbs: Optional[int]
    id_project: Optional[int]
    update_date: Optional[datetime]
    business_unit: Optional[str]
    constr_code: Optional[str]
    constr_name: Optional[str]
    constr_id: Optional[int]
    work_type_code: Optional[str]
    work_type_name: Optional[str]
    work_type_id: Optional[int]
    stage_code: Optional[str]
    stage_name: Optional[str]
    stage_id: Optional[int]
    contractor_code: Optional[str]
    contractor_name: Optional[str]
    contractor_id: Optional[int]
    mto_code: Optional[str]
    mto_name: Optional[str]
    mto_id: Optional[int]
    stage_ms_code: Optional[str]
    stage_ms_name: Optional[str]
    stage_ms_id: Optional[int]
    realisation_stage_code: Optional[str]
    realisation_stage_name: Optional[str]
    realisation_stage_id: Optional[int]
    fo_plan_text: Optional[str]
    fo_plan_number: Optional[float]
    fo_plan_date: Optional[datetime]
    fo_fact_text: Optional[str]
    fo_fact_number: Optional[float]
    fo_fact_date: Optional[datetime]
    fo_remaining_text: Optional[str]
    fo_remaining_number: Optional[float]
    fo_remaining_date: Optional[datetime]
    uom_text: Optional[str]
    uom_number: Optional[float]
    uom_date: Optional[datetime]
    note_text: Optional[str]
    note_number: Optional[float]
    note_date: Optional[datetime]
    shifr_rd_text: Optional[str]
    shifr_rd_number: Optional[float]
    shifr_rd_date: Optional[datetime]
    subcontractor_code: Optional[str]
    subcontractor_name: Optional[str]
    subcontractor_id: Optional[int]

    def to_db_update_model(self):
        source_dict = super().dict(
            by_alias=True, exclude={"id_activity", "business_unit"}
        )

        return source_dict

    def to_db_insert_model(self):
        source_dict = super().dict(by_alias=True, exclude={})

        return source_dict


class UDFCodeResource(BaseModel):
    id_resource: int
    update_date: Optional[datetime]
    business_unit: Optional[str]
    stg_code: Optional[str]
    stg_name: Optional[str]
    stg_id: Optional[int]
    accounting_code: Optional[str]
    accounting_name: Optional[str]
    accounting_id: Optional[int]
    is_fo_code: Optional[str]
    is_fo_name: Optional[str]
    is_fo_id: Optional[int]
    traffic_light_code: Optional[str]
    traffic_light_name: Optional[str]
    traffic_light_id: Optional[int]
    stg_type_code: Optional[str]
    stg_type_name: Optional[str]
    stg_type_id: Optional[int]
    specialty_code: Optional[str]
    specialty_name: Optional[str]
    specialty_id: Optional[int]

    def to_db_update_model(self):
        source_dict = super().dict(
            by_alias=True, exclude={"id_resource", "business_unit"}
        )

        return source_dict

    def to_db_insert_model(self):
        source_dict = super().dict(by_alias=True, exclude={})

        return source_dict


class UDFCodeResassignment(BaseModel):
    id_resassignment: int
    id_wbs: Optional[int]
    id_project: Optional[int]
    update_date: Optional[datetime]
    business_unit: Optional[str]
    change_coef_text: Optional[str]
    change_coef_number: Optional[float]
    change_coef_date: Optional[datetime]

    def to_db_update_model(self):
        source_dict = super().dict(
            by_alias=True, exclude={"id_resassignment", "business_unit"}
        )

        return source_dict

    def to_db_insert_model(self):
        source_dict = super().dict(by_alias=True, exclude={})

        return source_dict


class ExistingID(BaseModel):
    id: int


class DictionaryActivityCode(BaseModel):
    id: int
    Dictionary_Name: Optional[str]
    id_parent: Optional[int]
    code: Optional[str]
    name: Optional[str]
    full_code: Optional[str]
    id_wbs: Optional[int]
    id_project: Optional[int]
    update_date: Optional[datetime]
    business_unit: Optional[str]

    def to_db_update_model(self):
        source_dict = super().dict(by_alias=True, exclude={"id"})

        return source_dict

    def to_db_insert_model(self):
        source_dict = super().dict(by_alias=True, exclude={})

        return source_dict


class DictionaryProjectCode(BaseModel):
    id: int
    Dictionary_Name: Optional[str]
    id_parent: Optional[int]
    code: Optional[str]
    name: Optional[str]
    full_code: Optional[str]
    update_date: Optional[datetime]
    business_unit: Optional[str]

    def to_db_update_model(self):
        source_dict = super().dict(by_alias=True, exclude={"id"})

        return source_dict

    def to_db_insert_model(self):
        source_dict = super().dict(by_alias=True, exclude={})

        return source_dict


class DictionaryResourceCode(BaseModel):
    id: int
    Dictionary_Name: Optional[str]
    id_parent: Optional[int]
    code: Optional[str]
    name: Optional[str]
    full_code: Optional[str]
    update_date: Optional[datetime]
    business_unit: Optional[str]

    def to_db_update_model(self):
        source_dict = super().dict(by_alias=True, exclude={"id"})

        return source_dict

    def to_db_insert_model(self):
        source_dict = super().dict(by_alias=True, exclude={})

        return source_dict


class ActvRel(BaseModel):
    id_actvrel: int
    id_wbs: Optional[int]
    id_project: Optional[int]
    id_activity: Optional[int]
    pred_id_activity: Optional[int]
    pred_type: Optional[str]
    lag_hr_cnt: Optional[float]
    update_date: Optional[datetime]
    business_unit: Optional[str]

    def to_db_update_model(self):
        source_dict = super().dict(by_alias=True, exclude={"id_actvrel", "business_unit"})

        return source_dict

    def to_db_insert_model(self):
        source_dict = super().dict(by_alias=True, exclude={})

        return source_dict


class ResassignmentSpred(BaseModel):
    id_resassignment: int
    id_activity: Optional[int]
    id_resource: Optional[int]
    id_wbs: Optional[int]
    id_project: Optional[int]
    dt: Optional[datetime]
    target_qty: Optional[float]
    remain_qty: Optional[float]
    act_reg_qty: Optional[float]
    business_unit: Optional[str]
    update_date: Optional[datetime]
    id: Optional[int]

    def to_db_update_model(self):
        source_dict = super().dict(by_alias=True, exclude={"id_resassignment", "business_unit", "dt"})

        return source_dict

    def to_db_insert_model(self):
        source_dict = super().dict(by_alias=True, exclude={})

        return source_dict


class IFCBaseXMLModel(BaseModel):
    pass


class PeriodModel(BaseModel):
    StartDate: datetime
    EndDate: datetime
    PlannedUnits: float
    RemainingUnits: float


class ResourceAssignmentSpreadData(IFCBaseXMLModel):
    ResourceAssignmentObjectId: int
    StartDate: Optional[datetime]
    EndDate: Optional[datetime]
    PeriodType: Optional[str]
    Period: Optional[List[PeriodModel]]

    @validator("Period", pre=True)
    def check_period_data(cls, value):
        if isinstance(value, dict):
            return [value]
        return value


class ResourceAssignmentSpreadDataSet(IFCBaseXMLModel):
    ResourceAssignmentSpread: List[ResourceAssignmentSpreadData]


class ValidationResponse(BaseModel):
    table: str
    key: list
    reason: str
