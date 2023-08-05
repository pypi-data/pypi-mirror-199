import json
import humanize, math, sys, re, os, timeago
from appdirs import *
from amaz3dpy.clients import Amaz3DClient

from cmd import Cmd
from pyfiglet import Figlet
from InquirerPy import prompt
from clint.textui import colored
from columnar import columnar
from click import style
from dateutil import parser
from datetime import datetime, timezone
from InquirerPy import prompt
from InquirerPy.base.control import Choice
from InquirerPy.validator import EmptyInputValidator


from amaz3dpy.models import OptimizationOutputFormat, OptimizationParams, OptimizationNormalBakingParamsInput

class Cli(Cmd):

    @property
    def prompt(self):
        return '(amaz3d) '

    def _check_terms_of_service(self):
        tos = self._amaz3dclient.check_terms_of_service()
        if tos is not None:
            if tos.accepted is None:
                print(colored.red("Please read and accept the terms and conditions on https://amaz3d.adapta.studio/ to use AMAZ3d"))
                
                questions = [
                    {
                        "type": "confirm",
                        "message": "Do you want to log out?",
                        "name": "logout",
                        "default": True,
                    },
                ]

                result = prompt(questions)

                if result["logout"]:
                    self._amaz3dclient.logout()
                    
                self._amaz3dclient.close()
                sys.exit()

    def __init__(self):
        super().__init__()

        try:
            endpoint_info = json.load(open(self.__get_endpoint_path()))
        except:
            endpoint_info = {}

        self._amaz3dclient = Amaz3DClient(**endpoint_info)
        self._check_terms_of_service()
        f = Figlet(font='slant')
        self.intro = f.renderText('AMAZ3D') + "\nPowered By Adapta Studio\nType help or ? to list commands.\n"

    def do_exit(self, arg):
        '''Exit from AMAZ3D'''
        self._amaz3dclient.close()
        print('Thank you for using AMAZ3D')
        sys.exit()

    def do_clear_configurations(self, arg):
        '''Clear configurations'''
        questions = [
            {
                "type": "confirm",
                "message": "Do you want to clear all configurations:",
                "name": "confirm",
                "default": False,
            },
        ]

        result = prompt(questions)

        if result["confirm"]:
            self._amaz3dclient.clear_configs()

            try:
                os.remove(self.__get_endpoint_path())
            except:
                pass
            
            print(colored.green("Please restart to apply changes"))

    def __get_endpoint_path(self):
        appname = "amaz3dpy"
        appauthor = "Adapta Studio"
        app_path = user_data_dir(appname, appauthor)
        return os.path.join(app_path, "endpoint.json")

    def do_change_endpoint(self, arg):
        '''Change endpoint'''
        questions = [
            {
                "type": "input", 
                "message": "Endpoint:", 
                "default": "amaz3d_backend.adapta.studio",
                "name": "url",
            },
            {
                "type": "confirm",
                "message": "Use SSL:",
                "name": "use_ssl",
                "default": True,
            },
        ]

        result = prompt(questions)
        json.dump(result, open(self.__get_endpoint_path(), 'w'))
        print(colored.green("Endpoint changed successfully. Please restart to apply changes"))

    def do_login(self, arg):
        '''Perform login'''
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        questions = [
            {
                "type": "input", 
                "message": "Email:", 
                "name": "email",
                "validate": lambda result: re.fullmatch(email_regex, result),
                "invalid_message": "Invalid email address",
            },
            {
                "type": "password",
                "message": "Password:",
                "name": "password",
                "transformer": lambda _: "[hidden]",
            },
            {
                "type": "confirm",
                "message": "Keep me logged in",
                "name": "keep_the_user_logged_in",
                "default": True,
            },
        ]
        result = prompt(questions)
        login_result = self._amaz3dclient.login(**result) 
        if login_result:
            self._check_terms_of_service()
            print(colored.green("Log in succeeded"))
        else:
            print(colored.red("Unable to login"))

    def do_logout(self, arg):
        '''Perform logout'''
        questions = [
            {
                "type": "confirm",
                "message": "Are you sure you want to log out?",
                "name": "logout",
                "default": False,
            },
        ]

        result = prompt(questions)

        if result["logout"]:
            self._amaz3dclient.logout()
            print(colored.green("Log out succeeded"))

    def do_load_projects(self, arg):
        '''Load projects'''
        num = self._amaz3dclient.load_projects()
        if num:
            print(colored.green("Projects loaded: {0}".format(num)))
        else:
            print(colored.yellow("No projects loaded"))

    def do_projects(self, arg):
        '''View loaded projects'''
        now = datetime.utcnow()
        now = now.replace(tzinfo=timezone.utc)
        data = []

        for np in self._amaz3dclient.new_projects():
            data.append([
                f"{style(np.id, fg='yellow')}",
                np.name, 
                np.conversionStatus,
                np.objectModel.triangleCount if np.objectModel else "", 
                np.objectModel.fileSizeBytes if np.objectModel else "", 
                np.optimizationsCount if np.optimizationsCount is not None else 0, 
                timeago.format(parser.parse(np.lastActivityAt), now) if np.lastActivityAt is not None else ""
            ])

        for np in self._amaz3dclient.projects():
            data.append([
                f"{style(np.id, fg='blue')}", 
                np.name, 
                np.conversionStatus,
                np.objectModel.triangleCount, 
                np.objectModel.fileSizeBytes, 
                np.optimizationsCount if np.optimizationsCount is not None else 0, 
                timeago.format(parser.parse(np.lastActivityAt), now) if np.lastActivityAt is not None else ""
            ])

        if(len(data) == 0):
            print(colored.yellow("No projects available"))
            return

        table = columnar(data, headers=['Id', 'Name', 'Status', 'Triangles', 'Size', 'Exports created', 'Last Activity'], no_borders=True)
        print(table)

    def do_create_project(self, arg):
        '''Create a projects'''
        home_path = "~/" if os.name == "posix" else "C:\\"

        #estensioni primo file -> obj fbx gltf glb stl 3ds
        def file_validator_primary_file(result) -> bool:
            return os.path.isfile(os.path.expanduser(result)) and result.lower().endswith(('.obj', '.fbx', '.gltf', '.glb', '.stl', '.3ds'))

        # Extension: mtl, bin, jpg, jpeg, png
        def file_validator_secondary_file(result) -> bool:
            return os.path.isfile(os.path.expanduser(result)) and result.lower().endswith(('.mtl', '.bin', '.jpg', '.jpeg', '.png'))

        def check_files(file1, file2) -> bool:
            wallet = self._amaz3dclient.get_wallet()

            sum = 0
            for f in file2:
                try:
                    sum += os.path.getsize(os.path.expanduser(f))
                except OSError:
                    print(colored.red("Path '%s' does not exists or is inaccessible" %f))
                    return
            try:
                file1_size = os.path.getsize(os.path.expanduser(file1)) + sum
            except OSError:
                print(colored.red("Path '%s' does not exists or is inaccessible" %file1))
                return
            
            return file1_size > wallet.bytes_limit

        questions = [
            {
                "type": "input",
                "message": "Project name",
                "name": "name",
                "validate": lambda result: len(result) > 3,
            },
            {
                "type": "filepath",
                "message": "Object:",
                "name": "file_path",
                "default": home_path,
                "validate": file_validator_primary_file,
            },
        ]

        extra_questions = [
            {
                "type": "filepath",
                "message": "Object:",
                "name": "additional_file_path",
                "default": home_path,
                "validate": file_validator_secondary_file,
            },
        ]

        result = prompt(questions)
        
        additional_files_path = []
        answer = True

        while(answer):
            answer = input('Do you want to upload another file? (y/n): ').lower().strip() == 'y'
            if answer:
                additional_files_prompt = prompt(extra_questions)
                if additional_files_prompt['additional_file_path'] != home_path:
                    additional_files_path.append(additional_files_prompt['additional_file_path'])

        result['additional_files_path'] = additional_files_path

        if check_files(result["file_path"], result["additional_files_path"]):
            return
    
        res = self._amaz3dclient.create_project(**result)
        print(colored.green("Project {0} created successfully".format(res.id)))

    def do_select_project(self, arg):
        '''Select a projects'''
        questions = [
            {
                "type": "input",
                "message": "Project id",
                "name": "id",
            },
        ]

        result = prompt(questions)

        try:
            self._amaz3dclient.select_a_project(**result)
            print(colored.green("Project {0} selected".format(result["id"])))
        except ValueError as ex:
            print(colored.red(ex))

    def do_delete_selected_project(self, arg):
        '''Delete the selected project'''
        try:
            project = self._amaz3dclient.get_selected_project()
        except ValueError as ex:
            print(colored.red(ex))
            return

        questions = [
            {
                "type": "confirm",
                "message": "Are you sure you want to delete project {}?".format(project.id),
                "name": "confirm",
                "default": False,
            },
        ]

        result = prompt(questions)

        if not result['confirm']:
            return

        try:
            self._amaz3dclient.delete_selected_project()
            print(colored.green("Project {0} deleted successfully".format(project.id)))
        except ValueError as ex:
            print(colored.red(ex))

    def do_load_optimizations(self, arg):
        '''Load optimizations'''
        try:
            project = self._amaz3dclient.get_selected_project()
        except ValueError as ex:
            print(colored.red(ex))
            return

        num = self._amaz3dclient.load_optimizations()
        if num:
            print(colored.green("Optimizations for {1} loaded: {0}".format(num, project.id)))
        else:
            print(colored.yellow("No optimizations loaded for {0}".format(project.id)))

    def do_optimizations(self, arg):
        '''View optimizations'''
        try:
            project = self._amaz3dclient.get_selected_project()
        except ValueError as ex:
            print(colored.red(ex))
            return

        now = datetime.utcnow()
        now = now.replace(tzinfo=timezone.utc)
        data = []

        def format_parameters(parameters):
            return "Face reduction {0}\nFeature Importance {1}\nUV Seam Importance {2}\nMinimum Face Number {3}\nPreserve Boundary Edges {4}\nPreserve Hard Edges {5}\nPreserve Smooth Edges {6}\nDiscard UV {7}\nMerge Duplicated UV {8}\nRemove Isolated Vertices {9}\nRemove Non Manifold Faces {10}\nRemove Duplicated Faces {11}\nRemove Duplicated Boundary Vertices {12}\nRemove Degenerate Faces {13}\nRemove Meshes by Size {14}\nRemove Meshes by Count {15}\nProject Normals {16}\nUse Vertex Mask {17}\nResize Textures {18}\nNormals Weighting {19}\nContrast {20}\nJoined Simplification {21}\nNormals Importance {22}".format(
                    str(math.floor(parameters.face_reduction * 100))+"%",
                    "Low" if parameters.feature_importance == 0 else ("Med" if parameters.feature_importance == 1 else "High"),
                    "Low" if parameters.uv_seam_importance == 0 else ("Med" if parameters.uv_seam_importance == 1 else "High"),
                    parameters.minimum_face_number,
                    "low" if parameters.preserve_boundary_edges == 0 else ("Med" if parameters.preserve_boundary_edges == 1 else ("High" if parameters.uv_seam_importance == 2 else "Very High")),
                    "Yes" if parameters.preserve_hard_edges else "No",
                    "Yes" if parameters.preserve_smooth_edges else "No",
                    "No" if parameters.retexture else "Yes",
                    "Yes" if parameters.merge_duplicated_uv else "No",
                    "Yes" if parameters.remove_isolated_vertices else "No",
                    "Yes" if parameters.remove_non_manifold_faces else "No",
                    "Yes" if parameters.remove_duplicated_faces else "No",
                    "Yes" if parameters.remove_duplicated_boundary_vertices else "No",
                    "Yes" if parameters.remove_degenerate_faces else "No",
                    str(math.floor(parameters.remove_meshes_by_size * 100))+"%",
                    parameters.remove_meshes_by_count,
                    "Yes" if parameters.project_normals else "No",
                    "Yes" if parameters.use_vertex_mask is not None else "No",
                    parameters.resize_images,
                    "uniform" if parameters.normals_weighting == 0 else ("area" if parameters.normals_weighting == 1 else ("angle" if parameters.normals_weighting == 2 else "mixed")),
                    parameters.contrast,
                    "No" if parameters.joined_simplification else "Yes",
                    parameters.normals_scaling
                )

        for no in self._amaz3dclient.new_optimizations():
            data.append([
                f"{style(no.id, fg='yellow')}",
                no.name, 
                no.status,
                no.preset,
                None, 
                timeago.format(parser.parse(no.lastActivityAt), now) if no.lastActivityAt is not None else ""
            ])

        for no in self._amaz3dclient.optimizations():
            data.append([
                f"{style(no.id, fg='blue')}", 
                no.name, 
                no.status,
                no.preset,
                format_parameters(no.params) if no.params else "", 
                timeago.format(parser.parse(no.lastActivityAt), now) if no.lastActivityAt is not None else ""
            ])

        if(len(data) == 0):
            print(colored.yellow("No optimizations available"))
            return

        table = columnar(data, headers=['Id', 'Name', 'Status', 'Preset', 'Parameters', 'Last Activity'], no_borders=True, wrap_max=25)
        print(table)

    def do_create_optimization(self, arg):
        '''Create an optimization'''
        try:
            project = self._amaz3dclient.get_selected_project()
        except ValueError as ex:
            print(colored.red(ex))
            return

        try:
            wallet = self._amaz3dclient.get_wallet()
        except:
            print(colored.red("Unable to retrieve the credits left in your account"))
            return

        if (wallet.value == 0):
            print(colored.red("There are no credits left in your account"))
            return

        conversionExtAllowed = {
            "stl": ["orig", "obj"],
            "obj": ["orig", "stl", "gltf", "glb", "3ds", "obj", "fbx"],
            "gltf": ["orig", "obj", "fbx", "stl", "glb"],
            "glb": ["orig", "obj", "fbx", "stl", "gltf"],
            "3ds": ["orig", "obj"],
            "fbx": ["orig", "obj", "glb", "gltf", "stl"]
        }

        extensionChoiches = conversionExtAllowed[project.objectModel.name.split(".")[-1]]
        choices = []

        for i in extensionChoiches:
            # example: Choice("format_obj", name="obj"),
            choices.append(Choice("format_" + i, name=i))

        questions = [
            {
                "type": "input", 
                "message": "Optimization name:", 
                "name": "name",
                "validate": lambda result: len(result) > 3,
                "invalid_message": "Invalid optimization name",
            },
            {
                "type": "list",
                "message": "Which format to you want to convert the model into? (orig to keep the model unchanged)",
                "name": "format",
                "choices": choices,
                "multiselect": False,
            },
        ]

        name_format = prompt(questions)

        questions = [
            {
                "type": "number",
                "name": "face_reduction",
                "instruction": "0% - 99%",
                "message": "Face Reduction:",
                "min_allowed": 0,
                "max_allowed": 99,
                "default": 50,
                "float_allowed": False,
                "validate": EmptyInputValidator(),
                "filter": lambda result: f"{int(result) / 100}",
            },
            {
                "type": "number",
                "name": "feature_importance",
                "min_allowed": 0,
                "max_allowed": 2,
                "instruction": "0,1,2",
                "message": "Feature Importance:",
                "float_allowed": False,
                "validate": EmptyInputValidator(),
            },
            {
                "type": "number",
                "name": "preserve_boundary_edges",
                "min_allowed": 0,
                "max_allowed": 3,
                "instruction": "0,1,2,3",
                "message": "Preserve Boundary Edges",
                "float_allowed": False,
                "validate": EmptyInputValidator(),
            },
            {
                "type": "confirm",
                "message": "Preserve Hard Edges",
                "name": "preserve_hard_edges",
                "default": True,
            },
            {
                "type": "confirm",
                "message": "Preserve Smooth Edges",
                "name": "preserve_smooth_edges",
                "default": True,
            },
            {
                "type": "confirm",
                "message": "Retexture",
                "name": "retexture",
                "default": True,
            },
            {
                "type": "confirm",
                "message": "Merge Duplicated UV",
                "name": "merge_duplicated_uv",
                "default": False,
            },
            {
                "type": "confirm",
                "message": "Remove Isolated Vertices",
                "name": "remove_isolated_vertices",
                "default": True,
            },
            {
                "type": "confirm",
                "message": "Remove Non Manifold Faces",
                "name": "remove_non_manifold_faces",
                "default": True,
            },
            {
                "type": "confirm",
                "message": "Remove Duplicated Faces",
                "name": "remove_duplicated_faces",
                "default": True,
            },
            {
                "type": "confirm",
                "message": "Remove Duplicated Boundary Vertices",
                "name": "remove_duplicated_boundary_vertices",
                "default": True,
            },
            {
                "type": "confirm",
                "message": "Remove Degenerate Faces",
                "name": "remove_degenerate_faces",
                "default": True,
            },
            {
                "type": "number",
                "name": "uv_seam_importance",
                "instruction": "0,1,2",
                "message": "Set level of Uv Seam Importance",
                "min_allowed": 0,
                "max_allowed": 2,
                "float_allowed": False,
                "validate": EmptyInputValidator(),
            },
            {
                "type": "confirm",
                "message": "Preserve Project Normals?",
                "name": "project_normals",
                "default": False,
            },
            {
                "type": "number",
                "name": "resize_images",
                "instruction": "From 128 to 8192, 0 no resize",
                "message": "Resize Images?",
                "min_allowed": 0,
                "max_allowed": 8192,
                "float_allowed": False,
                "validate": EmptyInputValidator(),
            },
            {
                "type": "number",
                "name": "normals_weighting",
                "instruction": "0,1,2,3",
                "message": "Normals Weighting?",
                "min_allowed": 0,
                "max_allowed": 3,
                "float_allowed": False,
                "validate": EmptyInputValidator(),
            },
            {
                "type": "number",
                "name": "contrast",
                "instruction": "From -1 To 1:",
                "message": "Contrast?",
                "min_allowed": -1,
                "max_allowed": 1,
                "float_allowed": True,
                "validate": EmptyInputValidator(),
            },
            {
                "type": "confirm",
                "message": "Join simplification?",
                "name": "joined_simplification",
                "default": False,
            },
            {
                "type": "number",
                "name": "normals_scaling",
                "instruction": "0 - 1",
                "message": "Normals Scaling: ",
                "min_allowed": 0,
                "max_allowed": 1,
                "float_allowed": False,
                "validate": EmptyInputValidator(),
            },
            {
                "type": "number",
                "name": "remove_meshes_by_size",
                "instruction": "0% - 10%",
                "message": "Remove meshes by size: ",
                "min_allowed": 0,
                "max_allowed": 10,
                "float_allowed": False,
                "validate": EmptyInputValidator(),
                "filter": lambda result: f"{int(result) / 100}",
            },
            {
                "type": "number",
                "name": "remove_meshes_by_count",
                "instruction": "0 - 2000",
                "message": "Normals Scaling: ",
                "min_allowed": 0,
                "max_allowed": 2000,
                "float_allowed": False,
                "validate": EmptyInputValidator(),
            },
            {
                "type": "number",
                "name": "minimum_face_number",
                "instruction": "0 - 50",
                "message": "Minimum face number: ",
                "min_allowed": 0,
                "max_allowed": 50,
                "float_allowed": False,
                "validate": EmptyInputValidator(),
            },
        ]
        
        if project.allowsVertexMaskPolygonReduction:
            questions.append(
                {
                    "type": "confirm",
                    "message": "Use Vertex Mask?",
                    "name": "use_vertex_mask",
                    "default": False,
                },
            )

        parameters = prompt(questions)
        
        name = name_format['name']
        format = OptimizationOutputFormat[name_format['format']]
        params = OptimizationParams(**parameters)

        try:
            optimization = self._amaz3dclient.create_optimization(name, format, params=params)
        except Exception as ex:
            print(colored.red(ex))
            return

        print(colored.green("Optimization {0} created successfully".format(optimization.id)))
        pass

    def do_select_optimization(self, arg):
        '''Select an optimization'''
        try:
            project = self._amaz3dclient.get_selected_project()
        except ValueError as ex:
            print(colored.red(ex))
            return

        questions = [
            {
                "type": "input",
                "message": "Optimization id",
                "name": "id",
            },
        ]

        result = prompt(questions)

        try:
            self._amaz3dclient.select_an_optimization(**result)
            print(colored.green("Optimization {0} selected".format(result["id"])))
        except ValueError as ex:
            print(colored.red(ex))

    def do_create_normals_baking(self, arg):
        '''Create a normal bake'''
        try:
            project = self._amaz3dclient.get_selected_project()
            optimization = self._amaz3dclient.get_selected_optimization()
        except ValueError as ex:
            print(colored.red(ex))
            return

        if not project.allowsNormalsBaking:
            print(colored.yellow("the Model does not support normals baking..."))
            return
        
        choices = []
        for i in ['png', 'tga', 'jpg']:
            # example: Choice("format_obj", name="obj"),
            choices.append(Choice(i, name=i))

        questions = [
            {
                "type": "input", 
                "message": "Optimization name:", 
                "name": "name",
                "validate": lambda result: len(result) > 3,
                "invalid_message": "Invalid optimization name",
            },
        ]

        name_format = prompt(questions)
        name = name_format['name']

        questions = [
            {
                "type": "number",
                "name": "opacity",
                "instruction": "From 0 to 1",
                "message": "opacity",
                "min_allowed": 0,
                "max_allowed": 1,
                "float_allowed": True,
                "validate": EmptyInputValidator(),
            },
            {
                "type": "number",
                "name": "width",
                "instruction": "0 - 2048",
                "message": "width",
                "min_allowed": 0,
                "max_allowed": 2048,
                "default": 2048,
                "float_allowed": False,
                "validate": EmptyInputValidator(),
            },
            {
                "type": "number",
                "name": "height",
                "instruction": "0 - 2048",
                "message": "width",
                "min_allowed": 0,
                "max_allowed": 2,
                "default": 2048,
                "float_allowed": False,
                "validate": EmptyInputValidator(),
            },
            {
                "type": "number",
                "name": "normal_format",
                "instruction": "0 - openGL 1 - directX",
                "message": "normal_format",
                "min_allowed": 0,
                "max_allowed": 1,
                "float_allowed": False,
                "validate": EmptyInputValidator(),
            },
            {
                "type": "list",
                "message": "Image Format:",
                "name": "image_format",
                "choices": choices,
                "multiselect": False,
            },
        ]

        nbparameters = prompt(questions)
        nbparams = OptimizationNormalBakingParamsInput(**nbparameters)

        optimization = self._amaz3dclient.create_optimization(name, format="format_orig", nbparams=nbparams, relatedTo=optimization.id)
        if(optimization == 0):
            print(colored.yellow("Not enough credits to perform the operation"))
            return

        print(colored.green("Optimization {0} created successfully".format(optimization.id)))
        pass

    def do_download_selected_optimization(self, arg):
        '''Download selected optimization'''
        try:
            project = self._amaz3dclient.get_selected_project()
            optimization = self._amaz3dclient.get_selected_optimization()
        except ValueError as ex:
            print(colored.red(ex))
            return

        home_path = "~/" if os.name == "posix" else "C:\\"

        def file_name_validator(result) -> bool:
            if re.search(r'[^A-Za-z0-9_\-\\]',result):
                return False
            return True

        print(colored.green("Available downloads:\n\n"))
        available_downloads = self._amaz3dclient.view_available_downloads()
        for i in available_downloads:
            print(colored.green(i+": "+available_downloads[i]))

        print(colored.red("Warning: files will be overwritten!!"))

        questions = [
            {
                "type": "filepath",
                "message": "Directory to download files:",
                "name": "dst_path",
                "default": home_path,
                "only_directories": True,
            },
            {
                "type": "confirm",
                "message": "Download results files?",
                "name": "results_files",
                "default": False,
            },
            {
                "type": "confirm",
                "message": "Download converted files?",
                "name": "converted_files",
                "default": True,
            },
        ]

        result = prompt(questions)

        download_result = self._amaz3dclient.download_selected_optimization(**result)
        if download_result is None:
            print(colored.red("Error while writing file in " + str(result['dst_path'])))
        else:
            print(colored.green("Optimization {0} downloaded successfully".format(optimization.id)))

    def do_check_wallet(self, arg):
        '''Check your credits'''
        try:
            wallet = self._amaz3dclient.get_wallet()
        except Exception as e:
            print(colored.red(e))
            return None
        
        if(wallet.value == 0):
            print(colored.yellow("There are no credits left in your account"))
        elif(wallet.value == -9999):
            print(colored.green("Unlimited credits available on your account!"))
        else:
            print(colored.green("{0} credits left in your account".format(wallet.value)))
        print(colored.green("The next wallet renewal is going to be on {0}".format(wallet.expires)))
        print(colored.green("The maximum size for a project can be up to {0}".format(humanize.naturalsize(wallet.bytes_limit))))

    def do_load_presets(self, arg):
        '''Load presets'''
        
        num = self._amaz3dclient.load_optimization_templates()
        if num:
            print(colored.green("Presets loaded: {0}".format(num)))
        else:
            print(colored.yellow("No presets loaded"))
    
    def do_presets(self, arg):
        '''Check avaible presets'''
        data = []
        presets = self._amaz3dclient.optimization_templates()

        for e in presets:
            if len(e.optimizationTemplateItems) > 0:
                data.append([
                    f"{style(e.id, fg='blue')}", 
                    e.name,
                    e.description,
                    e.lastActivityAt,
                    len(e.optimizationTemplateItems)
                ])

        if(len(data) == 0):
            print(colored.yellow("No presets available"))
            return

        print("Presets with LODs")
        table = columnar(data, headers=['id', 'name', 'description', 'lastActivityAt', 'lods available'], no_borders=True)
        print(table)

    def do_select_preset(self, arg):
        '''Select an preset'''
        questions = [

            {
                "type": "input",
                "message": "Preset id",
                "name": "id",
            },
        ]

        result = prompt(questions)

        try:
            self._amaz3dclient.select_an_optimization_template(**result)
            print(colored.green("Optimization {0} selected".format(result["id"])))
        except ValueError as ex:
            print(colored.red(ex))

    def do_create_optimizations_from_preset(self, arg):
        '''Create optimizations from a preset'''
        try:
            project = self._amaz3dclient.get_selected_project()
            preset = self._amaz3dclient.get_selected_optimization_template()
        except ValueError as ex:
            print(colored.red(ex))
            return

        questions = [

            {
                "type": "input",
                "message": "Optimization from preset",
                "name": "name_optimizations",
            },
        ]

        result = prompt(questions)

        try:
            optimization = self._amaz3dclient.create_optimizations_from_preset(result["name_optimizations"])
            print(colored.green("Optimizations from preset created successfully"))
        except Exception as ex:
            print(colored.red(ex))