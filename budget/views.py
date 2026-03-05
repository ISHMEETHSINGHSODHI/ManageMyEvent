from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from .models import Project, Category, Expense
from django.views.generic import CreateView
from django.utils.text import slugify
from .forms import ExpenseForm
import json
from event_management_system import settings
# Create your views here.
import os
from django.http import HttpResponse
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from budget.models import Expense
from django_pandas.io import read_frame

# new code for charts
def export_data_and_generate_plots(request):
    
    queryset = Expense.objects.values('title', 'amount', 'project', 'category')
    df = read_frame(queryset)
    
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df = df.dropna(subset=['amount'])
    
    df_sorted = df.groupby('category')['amount'].sum().sort_values(ascending=False).reset_index()
    
    fig, axs = plt.subplots(1, 2, figsize=(14, 7))
    
    # Pie Chart
    df.groupby('title')['amount'].sum().plot(
        kind='pie', ax=axs[0], title='Amount Distribution by Category', autopct='%1.1f%%', colors=plt.cm.Paired.colors
    )
    axs[0].set_ylabel('')  # Hide y-label for pie chart
    
    # Bar Chart
    axs[1].bar(df_sorted['category'], df_sorted['amount'], color='skyblue', edgecolor='black')
    axs[1].set_title('Total Amount by Category')
    axs[1].set_ylabel('Amount')
    axs[1].set_xticklabels(df_sorted['category'], rotation=45, ha='right')  
    
    # Adjust layout
    plt.tight_layout()
    
    file_path = r'F:\Ishu\django\event_management_system\budget\static\img\report\chart.png'

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    plt.savefig(file_path)
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return HttpResponse(buffer, content_type='image/png')
# new code for charts end

# Download option start
from django.http import FileResponse
import os

def download_graph_view(request):
    file_path = r'F:\Ishu\django\event_management_system\budget\static\img\report\chart.png'

    # Check if the file exists
    if os.path.exists(file_path):
        # Return the file as a downloadable response
        response = FileResponse(open(file_path, 'rb'), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response
    else:
        return HttpResponse("File not found.", status=404)

# dowlload option ends
def project_list(request):
  
   
   project_list = Project.objects.all()
  
  
   return render(request,'budget/project-list.html',{'project_list':project_list})



def project_detail(request, project_slug):
  
   project = get_object_or_404(Project,slug=project_slug)
  
   
   if request.method == 'GET':
       category_list = Category.objects.filter(project=project)
       return render(request,'budget/project-detail.html',{'project':project, 'expense_list': project.expenses.all(), 'category_list':category_list})
  
   
   elif request.method == 'POST':
       
       form = ExpenseForm(request.POST)
       if form.is_valid():
          
          
           title = form.cleaned_data['title']
           amount = form.cleaned_data['amount']
           category_name = form.cleaned_data['category']
           category= get_object_or_404(Category, project = project, name= category_name)
          
           
           Expense.objects.create(
               project=project,
               title=title,
               amount=amount,
               category=category
           ).save()
          
  
   elif request.method == 'DELETE':
      
      
       id = json.loads(request.body)['id']
       expense = get_object_or_404(Expense,id =id)
       expense.delete()
       return HttpResponse('')
  
  
   return HttpResponseRedirect(project_slug)



class ProjectCreateView(CreateView):
  
  
   model = Project
   template_name = 'budget/add-project.html'
   fields = {'name','budget'}
  
  
   def form_valid(self, form):
       self.object = form.save(commit=False)
       self.object.save()


       categories = self.request.POST['categoriesString'].split(',')
      
       # Creating the categories and saving them
       for category in categories:
           Category.objects.create(
               project = Project.objects.get(id=self.object.id),
               name = category
           ).save()
       return HttpResponseRedirect(self.get_success_url())
  
   # Defining the get_success_url method to redirect to the project detail page
   def get_success_url(self):
       return slugify(self.request.POST['name'])

from django.core.mail import EmailMessage,send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.http import HttpResponse
import os

def homepage(request):
    subject = 'Please find the attached report'
    from_email = 'ajdjango3@gmail.com'
    to_email = ['ishmeetsinghsodhi14@gmail.com']

   
    file_name = 'chart.png' 
    file_path = os.path.join(settings.BASE_DIR, 'F:\\Ishu\\django\\event_management_system\\budget\\static\\img\\report', file_name)

   
    if os.path.exists(file_path):
        email = EmailMultiAlternatives(subject=subject, body='', from_email=from_email, to=to_email)
        email.attach_file(file_path)
        email.send()
        return HttpResponse('Mail sent successfully with the image.')
    else:
        return HttpResponse('Image file not found.', status=404)