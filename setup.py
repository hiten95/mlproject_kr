from setuptools import find_packages,setup


HYPHEN_E_DOT='-e .'
def get_requirements(file_path:str)->list:
    '''
    this function will return the list of requirements
    '''
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]
        
        if '-e .' in requirements:
            requirements.remove('-e .')
    
    return requirements



setup(
name='mlproject_kr',
version='0.0.1',
author='hiten prajapat',
author_email="donh4347@gmail.com",
packages=find_packages(),
install_requires=get_requirements('requirements.txt')




)