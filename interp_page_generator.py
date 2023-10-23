import dominate
from dominate.tags import *
import os


def get_interpretation_pages(project_interpretation_folder_path: str) -> list:
    """
    Find all the interpretation pages in the given folder path. Interpretation pages are HTML files that are generaeted by CATMA. 

    :param project_interpretation_folder_path: The path to the folder that contains all the interpretation pages for a project.
    """
    pages = []
    for file in os.listdir(project_interpretation_folder_path):
        if file.endswith('.html'):
            pages.append(file)

    return pages


def generate_overview_page_for_project(output_folder_path, project_name: str, project_interpretation_folder_path: str, project_interpretation_pages: list):
    doc = dominate.document(title=f'Visualization of Non-Conformances and Overview of interpretations generated for {project_name}')
    with doc.head:
        link(rel='stylesheet', href='css/overview_page_stylesheet.css')
    
    with doc:
        h1(f'Non-conformance visualization for {project_name}')
        with div(id='ncf_visualization'):
            visualize_ncf_path = project_interpretation_folder_path.split('interpretations')[0] + 'visualization/'
            img(src=f'{visualize_ncf_path}plantuml.png')
        h1(f'Overview of interpretations generated for {project_name}')
        with div(id='interpretations_list'):
            for page in project_interpretation_pages:
                splitted = page.split('_')
                if 'dynamic' in page:
                    ncf_type = 'dynamic'
                else:
                    ncf_type = 'static'

                involved_services = splitted[0] + ' and ' + splitted[1]
                capitalized_type = ncf_type.capitalize()
                h3(f'{capitalized_type} non-conformance between {involved_services}:')
                a('Click here to view the interpretation for the ' + ncf_type + ' non-conformance between ' + involved_services , href=f'{project_interpretation_folder_path}/{page}')

    with open(f'{output_folder_path}/{project_name}_overview.html', 'w') as f:
        f.write(doc.render())
    


def main():
    """
    This script is mainly used to generate a seperate HTML pages to list the interpretation of each project. As GitHub pages does not 
    allow us to get a directory view of subfolders, we would have to manually create this view ourselves.
    """
    examples_folder_path = 'interpretation_examples'
    projects = ['ewolff_microservice', 'shabbirdwd53_springboot-microservice', 'spring-petclinic_spring-petclinic-microservices', 'sqshq_piggymetrics']
    project_to_interp_pages_mapping = dict()
    for project in projects:
        project_to_interp_pages_mapping[project] = get_interpretation_pages(f'{examples_folder_path}/{project}/interpretations/')

    for project in project_to_interp_pages_mapping:
        generate_overview_page_for_project('./', project, f'{examples_folder_path}/{project}/interpretations', project_to_interp_pages_mapping[project])
    
    



if __name__ == '__main__':
    main()
