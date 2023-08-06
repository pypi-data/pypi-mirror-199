from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.db.models import Q
from custom.models import Department
from employee.models import Employee
from training.models import TCriteria, TrainingCriteria, TrainingPlan, TrainingEmp, ScholarshipPlan, ScholarshipEmp, ScholarshipEmpProgress, TrainingGap, TrainingDep, TrainingPlanGap
from django_summernote.widgets import SummernoteWidget

class DateInput(forms.DateInput):
	input_type = 'date'

class TrainingPlanForm(forms.ModelForm):
	start_date = forms.DateField(label='Data Hahu', widget=DateInput(), required=False)
	end_date = forms.DateField(label='Data Remata', widget=DateInput(), required=False)
	class Meta:
		model = TrainingPlan
		fields = ['type','year','subject','place', 'start_date','end_date','file']
	def __init__(self, unit, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['file'].label = 'Upload Pareser'
		self.fields['subject'].required = True
		self.fields['year'].required = True
		self.fields['type'].label = 'Hili Tipu Treinamento'
		self.fields['place'].required = True
		self.fields['type'].required = True
		self.fields['start_date'].required = True
		self.fields['end_date'].required = True
		self.fields['subject'].widget.attrs.update({'placeholder':'Prienche Materia Formasaun'})
		self.fields['place'].widget.attrs.update({'placeholder':'Prienche Fatin Treinamento'})
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('subject', css_class='form-group col-md-6 mb-0'),
				Column('place', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('type', css_class='form-group col-md-3 mb-0'),
				Column('year', css_class='form-group col-md-3 mb-0'),
				Column('start_date', css_class='form-group col-md-3 mb-0'),
				Column('end_date', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('file', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class TrainingEmpForm(forms.ModelForm):
	class Meta:
		model = TrainingEmp
		fields = ['employee']
	def __init__(self, unit, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['employee'].queryset = Employee.objects.filter(
			Q(status_id=1) & \
			Q(traininggap__isnull=True)
			).distinct().order_by('first_name')
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.fields['employee'].label='Hili Funsionario'
		self.helper.layout = Layout(
			Row(
				Column('employee', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)


class TrainingDepForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        label='Hili Ekipa'
    )
    
    class Meta:
        model = TrainingDep
        fields = ['department']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('department', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
        )



class TrainingEmpSubjectForm(forms.ModelForm):
	class Meta:
		model = TrainingEmp
		fields = ['subject']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['subject'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('subject', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class TrainingCritForm1(forms.ModelForm):
	class Meta:
		model = TrainingCriteria
		fields = ['criteria','obs']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['criteria'].queryset = TCriteria.objects.filter(category="Unidade").all()
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('criteria', css_class='form-group col-md-6 mb-0'),
				Column('obs', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class TrainingCritForm2(forms.ModelForm):
	class Meta:
		model = TrainingCriteria
		fields = ['criteria','obs']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['criteria'].queryset = TCriteria.objects.filter(category="RH").all()
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('criteria', css_class='form-group col-md-6 mb-0'),
				Column('obs', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class ScholarshipPlanForm(forms.ModelForm):
	start_date = forms.DateField(label='Data Hahu', widget=DateInput(), required=False)
	end_date = forms.DateField(label='Data Remata', widget=DateInput(), required=False)
	class Meta:
		model = ScholarshipPlan
		fields = ['subject','type','year','place','university','country', 'start_date','end_date','file']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['file'].label = 'Upload Pareser'
		self.fields['subject'].required = True
		self.fields['type'].required = True
		self.fields['year'].required = True
		self.fields['place'].required = True
		self.fields['university'].required = True
		self.fields['country'].required = True
		self.fields['start_date'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('subject', css_class='form-group col-md-8 mb-0'),
				Column('type', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('year', css_class='form-group col-md-3 mb-0'),
				Column('start_date', css_class='form-group col-md-3 mb-0'),
				Column('end_date', css_class='form-group col-md-3 mb-0'),
				Column('place', css_class='form-group col-md-3 mb-0'),
				
				css_class='form-row'
			),
			Row(
				Column('university', css_class='form-group col-md-4 mb-0'),
				Column('country', css_class='form-group col-md-4 mb-0'),
				Column('file', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class ScholarshipEmpForm(forms.ModelForm):
	class Meta:
		model = ScholarshipEmp
		fields = ['emp']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['emp'].queryset = Employee.objects.filter(status_id=1).all()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('emp', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)
class ScholarshipEmpThesisForm(forms.ModelForm):
	class Meta:
		model = ScholarshipEmp
		fields = ['thesis']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('thesis', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)
class ScholarshipEmpProgressForm(forms.ModelForm):
	date = forms.DateField(label='Data', widget=DateInput(), required=False)
	comment = forms.CharField(label="Remark", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	class Meta:
		model = ScholarshipEmpProgress
		fields = ['date', 'progress', 'comment']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('date', css_class='form-group col-md-6 mb-0'),
				Column('progress', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('comment', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)


class TrainingEmpGapForm(forms.ModelForm):
	class Meta:
		model = TrainingGap
		fields = ['comment']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['comment'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('comment', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)


class TrainingPlanEmpGapForm(forms.ModelForm):
	class Meta:
		model = TrainingPlanGap
		fields = ['gap']
		
	def __init__(self, unit, tplan, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['gap'].required = True
		self.plan = tplan
		self.fields['gap'].queryset = TrainingGap.objects.filter(
		Q(employee__curempdivision__unit=unit)
		
		).distinct().order_by('employee__first_name')
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('gap', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)
	
	def clean(self):
		cleaned_data = super().clean()
		gap = cleaned_data.get('gap')
		plan = self.plan
		# Check if the gap is already associated with the plan
		if gap and plan and TrainingPlanGap.objects.filter(gap=gap, plan=plan).exists():
			raise forms.ValidationError("This gap is already associated with the plan.")
		
		return cleaned_data


