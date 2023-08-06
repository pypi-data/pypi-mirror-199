import ast
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
import logging
from k3d.headless import k3d_remote
import socket
from contextlib import closing
from PIL import Image as PILImage
from io import BytesIO


def assign_last_line_into_variable(code):
    """Take the last command and assign it to a known variable name, if it's
    not already an assignment.

    If the last command includes the "display()" function call, remove it.

    Examples
    ========

    >>> code = "p = already_an_assignment(1, 2, kw1=True, kw2=False)"
    >>> assign_last_line_into_variable(code)
    p = already_an_assignment(1, 2, kw1=True, kw2=False)

    >>> code = "some_command(1, 2, kw1=True, kw2=False)"
    >>> assign_last_line_into_variable(code)
    myk3d = some_command(1, 2, kw1=True, kw2=False)

    >>> code = ""some_other_command.display()""
    >>> assign_last_line_into_variable(code)
    myk3d = some_other_command

    """
    tree = ast.parse(code)
    ln = tree.body[-1]
    if isinstance(ln, ast.Assign):
        return code
    
    if isinstance(ln, ast.Expr):
        if (isinstance(ln.value, ast.Call) and
            isinstance(ln.value.func, ast.Attribute) and 
            (ln.value.func.attr == "display")):
            # we are in this case: k3dplot.display(). Remove display()
            tree.body[-1] = ast.parse(ln.value.func.value.id).body[0]
        
        # make an assignment
        value = tree.body[-1].value if isinstance(tree.body[-1], ast.Expr) else tree.body[-1]
        tree.body[-1] = ast.Assign(
            targets=[ast.Name(id="myk3d")], 
            value=value,
            lineno=tree.body[-1].lineno
        )
    return ast.unparse(tree)


def set_camera_position(code, camera):
    """Assing the camera position to the correct attribute and trigger a
    rendering so that axis labels will be visibile.
    """
    tree = ast.parse(code)
    tree.body.append(ast.parse("myk3d.camera = %s" % camera).body[-1])
    tree.body.append(ast.parse("myk3d.render()").body[-1])
    return ast.unparse(tree)


def get_driver(browser, browser_path, driver_path, driver_options=[]):
    """Instantiate a webdriver.

    Parameters
    ----------

    browser : str
        Can be either ``"firefox"`` or ``"chrome"``.
    browser_path : str
        Location of the executable.
    driver_path : str
        Location of the driver.
    driver_options : list/tuple
        A list of strings to be added to the browser options with the
        ``add_argument`` method. Default to empty list.
    """
    if (browser is None) or (browser == "chrome"):
        logging.info("Browser: Chrome")
        options = webdriver.ChromeOptions()
        if driver_path is None:
            driver_path = ChromeDriverManager().install()
        service = ChromeService(driver_path)
        Browser = webdriver.Chrome
    else:
        logging.info("Browser: Firefox")
        options = webdriver.FirefoxOptions()
        if driver_path is None:
            driver_path = GeckoDriverManager().install()
        service = FirefoxService(driver_path)
        Browser = webdriver.Firefox

    logging.info("driver options: %s", driver_options)
    for do in driver_options:
        options.add_argument(do)

    if browser_path is not None:
        logging.info("browser_path: %s", browser_path)
        options.binary_location = browser_path
    logging.info("driver_path: %s", driver_path)

    # define a headless browser
    logging.info("Instantiating browser")
    driver = Browser(service=service, options=options)
    driver.set_window_position(0, 0)
    return driver


def get_port():
    """Return a new port to be used by a server process.

    Source: https://stackoverflow.com/a/45690594/2329968
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port = s.getsockname()[1]
        logging.info("Opening a new port: %s" % port)
        return port


def get_k3d_screenshot(driver, size, k3d_obj, camera_factor=None):
    """Retrieve a screenshot image from a K3D-Jupyter plot.

    Parameters
    ----------
    driver : selenium.webdriver
    size : (width, height)
        A 2-tuple specifying the window size in pixel
    k3d_obj : k3d.Plot
        A K3D-Jupyter's plot object.
    camera_factor : float
        Default to None, which is going to set ``camera_factor=1.5``.
    """
    logging.info("Generating a new screenshot:\n"
        "\tsize: %s\n\tcamera_factor: %s" % (size, camera_factor))
    if camera_factor is None:
        camera_factor = 1.5
    headless = k3d_remote(k3d_obj, driver, port=get_port(),
        width=size[0], height=size[1])
    headless.sync()
    headless.camera_reset(camera_factor)
    img = PILImage.open(BytesIO(headless.get_browser_screenshot()))
    headless.close()
    driver.quit()
    logging.info("Closing browser and returning image.")
    return img
