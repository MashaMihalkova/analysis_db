import os
import pandas as pd

from schemas import project
from db.database import SessionLocal
from db.models.etl import db_objects
from validation import objects as validation

# PATH_TO_LOG = 'log/'
# NAME_LOG = 'log_new.txt'


# TODO фильтр по id_wbs и id_proj

def init_validation(object_name, obj_instance, obj_instance_pmc, schema, validation_instance, id_wbs, id_proj):
    pk = db_objects.Project.metadata.tables[object_name].primary_key.columns.keys()
    with SessionLocal() as db:
        objects = db.query(obj_instance).all()
        # objects_pmc = db.query(obj_instance, obj_instance_pmc).filter(
        #     *[
        #         getattr(obj_instance, item) == getattr(obj_instance_pmc, item) for item in pk
        #     ]
        # ).all()

        df = []
        # for obj in objects_pmc:
        #     for item in obj._asdict().items():
        #         df.append(schema(**item[1]._asdict()).dict())
        # d_all_pmc = pd.DataFrame(df)

        df = [schema(**obj._asdict()).dict() for obj in objects if obj.id_wbs == id_wbs and obj.id_project == id_proj]
        # df = [schema(**obj._asdict()).dict() for obj in objects]
        d_all = pd.DataFrame(df)
        if d_all.values.shape[0] != 0:
            if len(pk) == 1:
                pk = pk[0]
            # type_error = validation_instance(d_all, object_name, pk, d_all_pmc)
            type_error = validation_instance(d_all, object_name, pk, id_wbs, id_proj)
            type_error.validate()

            return type_error.data


if __name__ == "__main__":
    if not os.path.exists(validation.PATH_TO_LOG):
        os.makedirs(validation.PATH_TO_LOG)
    with open('/'.join((validation.PATH_TO_LOG, validation.NAME_LOG)), 'a+') as fo:
        fo.write('[ \n')

    r = pd.DataFrame([])

    id_wbs = 1692103
    id_proj = 46538

    init_validation('project', db_objects.Project, db_objects.ProjectPMC, project.Project, validation.Project, id_wbs, id_proj)
    init_validation('activity', db_objects.Activity, db_objects.ActivityPMC, project.Activity, validation.Activity, id_wbs, id_proj)
    # init_validation('ISR', db_objects.ISR, db_objects.ISRPMC, project.ISR, validation.ISR, id_wbs, id_proj)
    init_validation('resource', db_objects.Resource, db_objects.ResourcePMC, project.Resource, validation.Resource, id_wbs, id_proj)
    init_validation('resassignment', db_objects.Resassignment, db_objects.ResassignmentPMC, project.Resassignment, validation.Resassignment, id_wbs, id_proj)
    init_validation('udf_code_project', db_objects.UDFCodeProject, db_objects.UDFCodeProjectPMC, project.UDFCodeProject, validation.UDFCodeProject, id_wbs, id_proj)
    init_validation('udf_code_activity', db_objects.UDFCodeActivity, db_objects.UDFCodeActivityPMC, project.UDFCodeActivity, validation.UDFCodeActivity, id_wbs, id_proj)
    init_validation('dictionary_activity_code', db_objects.DictionaryActivityCode, db_objects.DictionaryActivityCodePMC, project.DictionaryActivityCode, validation.DictionaryActivityCode, id_wbs, id_proj)
    init_validation('dictionary_project_code', db_objects.DictionaryProjectCode, db_objects.DictionaryProjectCodePMC, project.DictionaryProjectCode, validation.DictionaryProjectCode, id_wbs, id_proj)
    init_validation('dictionary_resource_code', db_objects.DictionaryResourceCode, db_objects.DictionaryResourceCodePMC, project.DictionaryResourceCode, validation.DictionaryResourceCode, id_wbs, id_proj)
    init_validation('udf_code_resource', db_objects.UDFCodeResource, db_objects.UDFCodeResourcePMC, project.UDFCodeResource, validation.UDFCodeResource, id_wbs, id_proj)
    init_validation('udf_code_resassignment', db_objects.UDFCodeResassignment, db_objects.UDFCodeResassignmentPMC, project.UDFCodeResassignment, validation.UDFCodeResassignment, id_wbs, id_proj)
    init_validation('actvrel', db_objects.ActvRel, db_objects.ActvRelPMC, project.ActvRel, validation.ActvRel, id_wbs, id_proj)
    init_validation('resassignmentspred', db_objects.ResassignmentSpred, db_objects.ResassignmentSpredPMC, project.ResassignmentSpred, validation.ResassignmentSpred, id_wbs, id_proj)

    with open('/'.join((validation.PATH_TO_LOG, validation.NAME_LOG)), 'a+') as fo:
        fo.write('] \n')
