
import threading
from amaz3dpy.auth import Auth
from amaz3dpy.projects import Projects
from amaz3dpy.models import LoginInput, Optimization, OptimizationNormalBakingParamsInput, OptimizationOutputFormat, OptimizationParams, OptimizationPreset, Project
from amaz3dpy.optimizations import ProjectOptimizations
from amaz3dpy.customer_wallet import CustomerWallet
from amaz3dpy.optimization_templates import OptimizationTemplates
from amaz3dpy.terms import Terms

class Amaz3DClient():

    def check_project_selected(func):
        def wrapper(*args, **kwargs):
            if not args[0].__selected_project:
                raise ValueError("No project selected")
            return func(*args, **kwargs)
        return wrapper

    def check_optimization_selected(func):
        def wrapper(*args, **kwargs):
            if not args[0].__selected_optimization:
                raise ValueError("No optimization selected")
            return func(*args, **kwargs)
        return wrapper

    def check_optimization_template_selected(func):
        def wrapper(*args, **kwargs):
            if not args[0].__selected_preset:
                raise ValueError("No optimization template selected")
            return func(*args, **kwargs)
        return wrapper

    def synchronized(func):
        def _synchronized(self, *args, **kw):
            with self._lock: 
                return func(self, *args, **kw)
        return _synchronized

    def __listen(self):

        def project_received(project):
                pass

        def optimization_received(optimization: Optimization):
            with self._lock:
                project = self.__projects.get(optimization.project.id)

                if project is None:
                    project = optimization.project
                    self.__projects.add_existing_item(project)

                if optimization.project.id not in self.__project_optimizations.keys():
                    self.__project_optimizations[project.id] = ProjectOptimizations(self.__auth, project)
                
                project_optimizations = self.__project_optimizations[project.id]
                project_optimizations.add_existing_item(optimization)

        def optimization_templates_received(optimization_templates: OptimizationTemplates):
            with self._lock:
                self.__optimization_templates = OptimizationTemplates(self.__auth)

        self.__projects.listen(project_received)
        self.__optimization_subscription.listen(optimization_received)
        self.__optimization_templates.listen(optimization_templates_received)

    def __stop_listen(self):
        self.__projects.stop_listen()
        self.__optimization_subscription.stop_listen()
        self.__optimization_templates.stop_listen()

    def __init__(self, url="amaz3d_backend.adapta.studio", use_ssl=True, disable_auto_update=False):
        self.__auth = Auth(url=url, use_ssl=use_ssl, refresh_token=True)
        self.__projects = Projects(self.__auth)
        self.__optimization_subscription = ProjectOptimizations(self.__auth)
        self.__project_optimizations = {}
        self.__selected_project = None
        self.__selected_optimization = None
        self.__wallet = CustomerWallet(self.__auth)
        self.__optimization_templates = OptimizationTemplates(self.__auth)
        self.__selected_preset = None
        self.__terms = Terms(self.__auth)
        self._lock = threading.Lock()
        if self.__auth.token_value:
            self.__listen()

    def close(self):
        self.__stop_listen()

    def __del__(self):
        self.close()

    def login(self, email, password, keep_the_user_logged_in=True) -> bool:
        self.__auth.login_input = LoginInput(**{
            'email': email,
            'password': password,
        })
        if keep_the_user_logged_in:
            self.__auth.save_refresh_token()
        result = self.__auth.login()
        self.__listen()

        if result is not None:
            return True

        return False

    def logout(self):
        self.__auth.clear_credentials()
        self.__auth.clear_refresh_token()
        self.__auth.clear()

    def clear_configs(self):
        self.__auth.clear_configs()

    @synchronized
    def new_projects(self):
        return self.__projects.list_new()

    @synchronized
    def projects(self):
        return self.__projects.list()

    @synchronized
    def clear_projects(self):
        self.__projects.clear()

    @synchronized
    def load_projects(self):
        return self.__projects.load_next()

    @synchronized
    def load_project_by_id(self, id: str):
        return self.__projects.load_by_id(id)

    @synchronized
    def create_project(self, name: str, file_path: str, additional_files_path = {}) -> Project:
        return self.__projects.create_project(name=name, file_path=file_path, additional_files_path=additional_files_path)

    @synchronized
    @check_project_selected
    def delete_selected_project(self):
        self.__projects.delete_project(self.__selected_project)
        self.__selected_project = None

    @synchronized
    def select_a_project(self, id: str):
        selected = self.__projects.get(id)

        if selected is None:
            raise ValueError("Project not found")

        self.__selected_project = selected.id
        self.__selected_optimization = None

        if selected.id not in self.__project_optimizations.keys():
            self.__project_optimizations[selected.id] = ProjectOptimizations(self.__auth, selected)

        return self

    @synchronized
    @check_project_selected
    def get_selected_project(self):
        selected = self.__projects.get(self.__selected_project)

        if selected is None:
            raise ValueError("Project not found")

        return selected

    @synchronized
    @check_project_selected
    def optimizations(self):
        return self.__project_optimizations[self.__selected_project].list()

    @synchronized
    @check_project_selected
    def new_optimizations(self):
        return self.__project_optimizations[self.__selected_project].list_new()

    @synchronized
    @check_project_selected
    def clear_optimizations(self):
        self.__project_optimizations[self.__selected_project].clear()

    @synchronized
    @check_project_selected
    def load_optimizations(self):
        return self.__project_optimizations[self.__selected_project].load_next()

    @synchronized
    @check_project_selected
    def create_optimization(self, name, format: OptimizationOutputFormat, nbparams: OptimizationNormalBakingParamsInput = None, params: OptimizationParams = None, preset: OptimizationPreset = None, relatedTo: str = None):
        if nbparams is None and params is None and preset is None:
            raise ValueError("EITHER nbparams OR parameters OR preset have to be provided")

        project_optimizations: ProjectOptimizations = self.__project_optimizations[self.__selected_project]

        if params:
            return project_optimizations.create_optimization(name=name, outputFormat=format, params=params)

        if nbparams:
            return project_optimizations.create_optimization(name=name, outputFormat=format, nbparams=nbparams, relatedTo_id=relatedTo)

        
        return project_optimizations.create_optimization(name=name, outputFormat=format, preset=preset)
    
    @synchronized
    @check_project_selected
    def select_an_optimization(self, id: str):
        selected = self.__project_optimizations[self.__selected_project].get(id)

        if selected is None:
            raise ValueError("Optimization not found in this project")

        self.__selected_optimization = selected.id
        return self

    def __get_selected_optimization(self):
        selected = self.__project_optimizations[self.__selected_project].get(self.__selected_optimization)

        if selected is None:
            raise ValueError("Optimization not found")

        return selected

    @synchronized
    @check_project_selected
    @check_optimization_selected
    def get_selected_optimization(self):
        return self.__get_selected_optimization()

    @synchronized
    @check_project_selected
    @check_optimization_selected
    def view_available_downloads(self):
        project_optimizations: ProjectOptimizations = self.__project_optimizations[self.__selected_project]
        optimization = self.__get_selected_optimization()
        return project_optimizations.view_downloads(optimization)

    @synchronized
    @check_project_selected
    @check_optimization_selected
    def download_selected_optimization(self, dst_file_path=None, dst_path=None, results_files=False, converted_files=True, additionals=True):
        project_optimizations: ProjectOptimizations = self.__project_optimizations[self.__selected_project]
        optimization = self.__get_selected_optimization()
        return project_optimizations.download_result(optimization, dst_file_path=dst_file_path, dst_path=dst_path, results_files=results_files,  converted_files=converted_files, additionals=additionals)

    @synchronized
    def get_wallet(self):
        return self.__wallet.retrive()

    @synchronized
    def load_optimization_templates(self):
        return self.__optimization_templates.load_next()

    @synchronized
    def optimization_templates(self):
        return self.__optimization_templates.list()

    @synchronized
    def select_an_optimization_template(self, id: str):
        selected = self.__optimization_templates.get(id)

        if selected is None:
            raise ValueError("Preset not found")

        if len(selected.optimizationTemplateItems) == 0:
            raise ValueError("Please select another preset with lods")

        self.__selected_preset = selected.id
        return self

    @synchronized
    @check_project_selected
    @check_optimization_template_selected
    def create_optimizations_from_preset(self, name_optimizations, selected_project_id: str = None, preset_id: str = None):
        if selected_project_id is None:
            selected_project_id = self.__selected_project
        if preset_id is None:
            preset_id = self.__selected_preset
    
        return self.__optimization_templates.create_optimizations_from_template(name_optimizations, selected_project_id, preset_id)

    @synchronized
    @check_optimization_template_selected
    def get_selected_optimization_template(self):
        selected = self.__optimization_templates.get(self.__selected_preset)

        if selected is None:
            raise ValueError("Optimization Template not found")

        return selected
    
    @synchronized
    def check_terms_of_service(self):
        return self.__terms.user_info_related_to_terms_and_conditions()