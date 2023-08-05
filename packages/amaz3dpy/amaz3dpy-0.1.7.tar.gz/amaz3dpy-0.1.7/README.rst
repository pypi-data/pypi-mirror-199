================
AMAZ3DPY
================

Introduction
============
amaz3dpy is a Python SDK to interact with Amaz3d Web APIs.
This SDK is built by three main component:

- Object primitives for dealing with Authentication, Projects and Optimizations
- A simple Client that simplifies interaction with Web APIs providing authentication, projects handling (visualization, creation, etc.), optimizations handling (creation and download)
- A cli command for using Amaz3D from a terminal session

*Please consider that an Amaz3d account is required for using all functionalities*

*For further information visit:* `Adapta Studio Website <https://adapta.studio>`_

Object primitives
=================
amaz3dpy provides primitives for interacting with Amaz3d functionalities.
Here you can find the import statements for the main objects:

.. code-block:: python

    from amaz3dpy.auth import Auth
    from amaz3dpy.projects import Projects
    from amaz3dpy.models import LoginInput, Optimization, OptimizationNormalBakingParamsInput, OptimizationOutputFormat, OptimizationParams, OptimizationPreset, Project
    from amaz3dpy.optimizations import ProjectOptimizations
    from amaz3dpy.customer_wallet import CustomerWallet
    from amaz3dpy.optimization_templates import OptimizationTemplates
    from amaz3dpy.terms import Terms

Client
======
The client encapsulates object primitives to follow the application business logic:

.. code-block:: python

    from amaz3dpy.clients import Amaz3DClient
    from amaz3dpy.models import OptimizationOutputFormat, OptimizationParams, OptimizationPreset

    amaz3dclient = Amaz3DClient()
    amaz3dclient.login(email="your@email.com",password="mypass")

    my_project = {"name": "My project", "file_path":"/path/to/file"}
    amaz3dclient.create_project(**my_project)

    amaz3dclient.load_projects()
    print(amaz3dclient.projects()

    amaz3dclient.select_a_project(id="....id.....")
    amaz3dclient.load_optimizations()
    print(amaz3dclient.optimizations())

    format = OptimizationOutputFormat['format_orig']
    params = OptimizationParams()
    params.face_reduction = 0.5
    params.feature_importance = 0
    params.preserve_hard_edges = False
    ....
    optimization = amaz3dclient.create_optimization("my optimization", format, params=params)

    amaz3dclient.select_an_optimization(id=".....id......")
    amaz3dclient.download_selected_optimization(dst_path="/my/path")

Cli
===
It is possible to run a simple interactive CLI application for creating projects and optimizations.
Open your terminal and run:

::

    amaz3d

Login
----------

Run the *login* command, and insert your credentials

Projects management
-------------------

It is possible to load and view projects by running *load_projects* and *projects*

The first command loads projects page by page.

The second command instead prints all projects loaded.

*create_project* is used to create a new project and to upload an object that could be optimized afterwards

Optimizations management
------------------------

Before creating or visualizing optimization it is necessary to select a project with *select_project* command.

Optimization visualization follows the same logic of projects: use *load_optimizations* and *optimizations* commands

*create_optimization* is used to create an optimization for the selected project. It is possible to create optimization by selecting a preset or by tweaking advanced parameters

Downlaod an optimization
------------------------

To download an optimization it is necessary to select it first using the *select_optimization* command.
After that an optimization is selected it is possible to download the result with the *download_selected_optimization* command.

Help 
------------------------
Type help to get a list of available commands