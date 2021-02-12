from django import forms
from django.forms import formset_factory
from django.forms import BaseFormSet
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class tclInputForm(forms.ModelForm):
    class Meta:
        model = tclInput
        fields = ('meshFile', 'kernelType', 'packetCount')
        kernel_choices = (('TetraSVKernel','TetraSVKernel'),
                         ('TetraSurfaceKernel','TetraSurfaceKernel'),
                         ('TetraVolumeKernel','TetraVolumeKernel'),
                         ('TetraInternalKernel','TetraInternalKernel'))
        widgets = {
            'kernelType': forms.Select(choices=kernel_choices),
        }

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial['packetCount'] = 1000000
        kwargs['initial'] = initial
        super(tclInputForm, self).__init__(*args, **kwargs)
        self.fields['meshFile'].required = False

class presetForm(forms.ModelForm):
    class Meta:
        model = preset
        fields = ('presetMesh', 'layerDesc')

class materialSet(forms.Form):
    layer = forms.CharField(label='Layer', required = False, max_length=255)
    custom = forms.ModelChoiceField(label='Preset', queryset=Material.objects.all(), required = False)
    material = forms.CharField(label='Material',
                               widget=forms.TextInput(attrs={
                                                      'class': 'form-control',
                                                      'placeholder': 'Enter Material Name here'
                                                      }),
                               max_length=255)
    scatteringCoeff = forms.FloatField(label='Scattering Coefficient', min_value=0)
    absorptionCoeff = forms.FloatField(label='Absorption Coefficient', min_value=0)
    refractiveIndex = forms.FloatField(label='Refractive Index', min_value=1)
    anisotropy = forms.FloatField(label='Anisotropy', min_value=-1, max_value=1)

class materialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ('material_name', 'scattering_coeff', 'absorption_coeff', 'refractive_index', 'anisotropy')

class pdtForm(forms.Form):
    opt = forms.ChoiceField(label="Optical File", 
                            help_text="Available optical files.")
    mesh = forms.ChoiceField(label="Mesh File", 
                            help_text="Available mesh files.")
    total_energy = forms.CharField( label='Total Energy', required = True, max_length=255, 
                                    help_text="Unitless number used by the simulator to scale the light dose thresholds to match the unit of the light-simulator output. <br />Typically in the range of 1e6 to 1e11.")
    num_packets = forms.CharField(label='Num Packets', required = True, max_length=255, 
                                    help_text="The number of photon packets to launch in the light simulator FullMonte. Typically it is around 1e5 to 1e6.")
    wave_length = forms.CharField(label='Wave Length', required = True, max_length=255, 
                                    help_text="Activation wavelength of the Photosensitizer.")
    tumor_weight = forms.CharField(label='Tumor Weight', required = True, max_length=255, 
                                    help_text="An importance weight given to the tumor tissue to give it priority in the optimization.")
    
    # light_placement_file = forms.FileField(label='light_placement_file')

    def __init__(self, opt_list=None, mesh_list=None, *args, **kwargs):
        super(pdtForm, self).__init__(*args, **kwargs)
        choice_opt = [(opt_name, opt_name) for opt_name in opt_list]
        if opt_list:
            self.fields['opt'].choices = choice_opt
        choice_mesh = [(mesh_name, mesh_name) for mesh_name in mesh_list]
        if mesh_list:
            self.fields['mesh'].choices = choice_mesh
        
class pdtPlaceFile(forms.Form):
    placement_type = forms.ChoiceField(label='Placement Type', choices=(('fixed','fixed'),
                                                                        ('virtual', 'virtual'),),
                                        help_text="Specifies the type of placement for the sources. <br />If it is fixed, please palce sources at fixed position in INIT_PLACEMENT_FILE. <br />If it is virtual and SOURCE_TYPE is point, the tool will fill the mesh with candidate point sources.")
    source_type = forms.ChoiceField(label='Source Type', choices=(('point','point'),
                                                                        ('line', 'line'),),help_text="The type of light sources used. ")
    light_placement_file = forms.FileField(
        label='Placement File',
        help_text="Placement of intial light sources."
    )

class mosekLicense(forms.Form):
    mosek_license = forms.FileField(
        label='Mosek license'
    )
        

class lightSource(forms.Form):
    sourceType = forms.ChoiceField(label='Type', choices=(('Point','Point'),
                                                          ('PencilBeam','PencilBeam'),
                                                          ('Volume','Volume'),
                                                          ('Ball','Ball'),
                                                          #('Line','Line'),
                                                          #('Fiber','Fiber'),
                                                          #('Tetraface','Tetraface'),
                                                          #('Composite','Composite')
                                                          ))
    # for Point
    xPos = forms.FloatField(label='X Position', widget=forms.TextInput(attrs={'placeholder': 'x'}), required=False)
    yPos = forms.FloatField(label='Y Position', widget=forms.TextInput(attrs={'placeholder': 'y'}), required=False)
    zPos = forms.FloatField(label='Z Position', widget=forms.TextInput(attrs={'placeholder': 'z'}), required=False)

    # for Pencil Beam (Position uses xyz from point)
    xDir = forms.FloatField(label='X Direction', widget=forms.TextInput(attrs={'placeholder': 'x'}), required=False)
    yDir = forms.FloatField(label='Y Direction', widget=forms.TextInput(attrs={'placeholder': 'y'}), required=False)
    zDir = forms.FloatField(label='Z Direction', widget=forms.TextInput(attrs={'placeholder': 'z'}), required=False)

    # for Volume
    vElement = forms.IntegerField(label='V Element ID', required=False)

    # for Ball (center uses xyz from point)
    rad = forms.FloatField(label='Radius', required=False)

    # for Line


    power = forms.IntegerField(label='Power', required=False, initial=1)

class RequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text='Required.')
    last_name = forms.CharField(max_length=30, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Required.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class awsFiles(forms.ModelForm):
    class Meta:
        model = awsFile
        fields = ('DNS', 'pemfile', 'TCP_port')
    def __init__(self, *args, **kwargs):
        super(awsFiles, self).__init__(*args, **kwargs)

class visualizeMeshForm(forms.ModelForm):
    class Meta:
        model = visualizeMesh
        fields = ('outputMeshFile',)
    def __init__(self, *args, **kwargs):
        super(visualizeMeshForm, self).__init__(*args, **kwargs)

materialSetSet = formset_factory(materialSet, formset=RequiredFormSet)
lightSourceSet = formset_factory(lightSource, formset=RequiredFormSet)
