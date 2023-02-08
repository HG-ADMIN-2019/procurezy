from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models.application_data import ProjectDetails

django_query_instance = DjangoQueries()


def save_project_to_db(project_data):
    """

    """
    project_detail = project_data['project_data']
    if project_data['project_action'] == 'UPDATE':
        django_query_instance.django_update_query(ProjectDetails,
                                                  {'client': global_variables.GLOBAL_CLIENT,
                                                   'project_id': project_detail['project_id']},
                                                  {'project_name': project_detail['project_name'],
                                                   'project_desc': project_detail['project_description'],
                                                   'start_date': project_detail['start_date'],
                                                   'end_date': project_detail['end_date']})
    else:
        project_dictionary = {'project_detail_guid': guid_generator(),
                              'client': global_variables.GLOBAL_CLIENT,
                              'project_id': project_detail['project_id'],
                              'project_name': project_detail['project_name'],
                              'project_desc': project_detail['project_description'],
                              'start_date': project_detail['start_date'],
                              'end_date': project_detail['end_date']}
        django_query_instance.django_create_query(ProjectDetails, project_dictionary)
    project_data_response = django_query_instance.django_filter_query(ProjectDetails,
                                                                      {'del_ind': False,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      None, None)

    return project_data_response


def get_project_filter_list(filter, query_count):
    """

    """
    project_details = django_query_instance.django_filter_query_with_entry_count(ProjectDetails, filter, ['project_id'], None,
                                                                                 int(query_count))

    return project_details
