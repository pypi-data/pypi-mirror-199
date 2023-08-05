from amaz3dpy.clients import Cli
from amaz3dpy.auth import Auth
from amaz3dpy.customer_wallet import CustomerWallet
from amaz3dpy.models import CursorPaging, LoginInput, CreateOneOptimizationTemplateInput, OptimizationTemplateFilter,  OptimizationTemplateSort, CreateOneOptimizationTemplateItemInput
from amaz3dpy.optimization_templates import OptimizationTemplates

def amaz3d():
    Cli().cmdloop()