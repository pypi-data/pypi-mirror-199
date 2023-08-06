import os
from ..download import download_full_site, InjectDirective
from ..deploy.ftp import deploy_to_ftp

def update_site_ftp(project_root_folder: str, site_url: str, ftp_host: str, ftp_user: str, ftp_pwd: str, site_relative_path: str = None, force_download: bool = False, google_analytics_id: str = None, save_html_as: str = 'index.html', links_to_force_open_in_current_tab: list[list] = [], inject_directives: list[InjectDirective] = []):
    download_full_site(
        url=site_url,
        project_root_folder=project_root_folder,
        site_relative_path=site_relative_path,
        force_download=force_download,
        google_analytics_id=google_analytics_id,
        save_html_as=save_html_as,
        links_to_force_open_in_current_tab=links_to_force_open_in_current_tab,
        inject_directives=inject_directives
    )
    deploy_to_ftp(
        host=ftp_host,
        user=ftp_user,
        password=ftp_pwd,
        base_folder=project_root_folder
    )
