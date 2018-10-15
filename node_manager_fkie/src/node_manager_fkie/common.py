import os
import rospy

import node_manager_fkie as nm

MANIFEST_FILE = 'manifest.xml'
PACKAGE_FILE = 'package.xml'

try:
    from catkin_pkg.package import parse_package
    CATKIN_SUPPORTED = True
except ImportError:
    CATKIN_SUPPORTED = False

PACKAGE_CACHE = {}


def utf8(s, errors='replace'):
    '''
    Converts string to unicode.
    '''
    if isinstance(s, (str, buffer)):
        return unicode(s, "utf-8", errors=errors)
    elif not isinstance(s, unicode):
        return unicode(str(s))
    return s


def get_ros_home():
    '''
    Returns the ROS HOME depending on ROS distribution API.

    :return: ROS HOME path
    :rtype: str
    '''
    try:
        import rospkg.distro
        distro = rospkg.distro.current_distro_codename()
        if distro in ['electric', 'diamondback', 'cturtle']:
            import roslib.rosenv
            return roslib.rosenv.get_ros_home()
        else:
            from rospkg import get_ros_home
            return get_ros_home()
    except Exception:
        from roslib import rosenv
        return rosenv.get_ros_home()


def get_rosparam(param, masteruri):
    '''
    Get parameter using :class:`rospy.msproxy.MasterProxy`
    '''
    if masteruri:
        try:
            master = rospy.msproxy.MasterProxy(masteruri)
            return master[param]  # MasterProxy does all the magic for us
        except KeyError:
            return {}


def delete_rosparam(param, masteruri):
    '''
    Delete parameter using :class:`rospy.msproxy.MasterProxy`
    '''
    if masteruri:
        try:
            master = rospy.msproxy.MasterProxy(masteruri)
            del master[param]  # MasterProxy does all the magic for us
        except Exception:
            pass


def to_url(path):
    '''
    Searches the package name for given path and create an URL starting with pkg://

    :see: uses :meth:`package_name`
    '''
    result = path
    pkg, pth = package_name(os.path.dirname(path))
    if pkg is not None:
        result = "pkg://%s%s" % (pkg, path.replace(pth, ''))
    return result


def package_name(path):
    '''
    Returns for given directory a tuple of package name and package path or None values.
    The results are cached!

    :rtype: tuple(name, path)
    '''
    return (nm.nmd().package_name(path), path)


def is_package(file_list):
    return (MANIFEST_FILE in file_list or (CATKIN_SUPPORTED and PACKAGE_FILE in file_list))
