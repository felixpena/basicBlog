from django.shortcuts import render

# Create your views here.

from django.views import generic
from .models import Blog, BlogAuthor, BlogComment
from django.contrib.auth.models import User #Blog author or commenter

################## min 57 video: 36945 - 08/06 - Playground Avanzado (parte 2)- Pantalla compartida con vista del orador
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            context = {"message": f"Usuario credado, Bienvenido {username}"}
            return render(request, 'index.html', context = context)
        else:
            errors = form.errors
            form = UserCreationForm()
            context = {"errors": errors, "form": form}
            return render(request, 'registration/register.html', context = context)
    else:
        form = UserCreationForm()
        context = {'form': form}
        return render(request, 'registration/register.html', context = context)
###################

def index(request):
    """
    View function for home page of site.
    """
    # Render the HTML template index.html
    return render(request,'index.html',)
    

class BlogListView(generic.ListView):
    """
    Generic class-based view for a list of all blogs.
    Vista genérica basada en la clase para una lista de todos los blogs.

    La clase ListView, Renderiza alguna lista de objetos, establecida por `self.model` o `self.queryset`.
    `self.queryset` puede ser cualquier iterable de elementos, no sólo un queryset.
    """
    model = Blog
    paginate_by = 5

    
from django.shortcuts import get_object_or_404

class BlogListbyAuthorView(generic.ListView):
    """
    Generic class-based view for a list of blogs posted by a particular BlogAuthor.
    Vista genérica basada en clases para una lista de blogs publicados por un determinado BlogAuthor.
    """
    model = Blog
    paginate_by = 5
    template_name ='blog/blog_list_by_author.html'
    
    def get_queryset(self):
        """
        Return list of Blog objects created by BlogAuthor (author id specified in URL)
        Devuelve la lista de objetos Blog creados por BlogAuthor (id de autor especificado en la URL)
        """
        id = self.kwargs['pk']
        target_author=get_object_or_404(BlogAuthor, pk = id)
        return Blog.objects.filter(author=target_author)
        
    def get_context_data(self, **kwargs):
        """
        Add BlogAuthor to context so they can be displayed in the template
        Añadir BlogAuthor al contexto para que se puedan mostrar en la plantilla
        """
        # Call the base implementation first to get a context    
        # Llama primero a la implementación base para obtener un contexto
        context = super(BlogListbyAuthorView, self).get_context_data(**kwargs)
        # Get the blogger object from the "pk" URL parameter and add it to the context
        context['blogger'] = get_object_or_404(BlogAuthor, pk = self.kwargs['pk'])
        return context
    
    

class BlogDetailView(generic.DetailView):
    """
    Generic class-based detail view for a blog.
    """
    model = Blog

    
class BloggerListView(generic.ListView):
    """
    Generic class-based view for a list of bloggers.  
    Vista genérica basada en clases para una lista de bloggers.
    """
    model = BlogAuthor
    paginate_by = 5


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse


class BlogCommentCreate(LoginRequiredMixin, CreateView):
    """
    Form for adding a blog comment. Requires login.
    Formulario para añadir un comentario en el blog. Requiere inicio de sesión. 
    """
    model = BlogComment
    fields = ['description',]

    def get_context_data(self, **kwargs):
        """
        Add associated blog to form template so can display its title in HTML.
        Añade el blog asociado a la plantilla del formulario para poder mostrar su título en HTML.
        """
        # Call the base implementation first to get a context 
        # Llama primero a la implementación base para obtener un contexto
        context = super(BlogCommentCreate, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context 
        # Obtenga el blog de id y añádalo al contexto
        context['blog'] = get_object_or_404(Blog, pk = self.kwargs['pk'])
        return context
        
    def form_valid(self, form):
        """
        Add author and associated blog to form data before setting it as valid (so it is saved to model)
        Añadir el autor y el blog asociado a los datos del formulario antes de establecerlo como válido 
        (para que se guarde en el modelo)
        """
        #Add logged-in user as author of comment 
        # Añadir el usuario conectado como autor del comentario
        form.instance.author = self.request.user
        #Associate comment with blog based on passed id   
        # Asociar el comentario con el blog en base a la identificación pasada
        form.instance.blog=get_object_or_404(Blog, pk = self.kwargs['pk'])
        # Call super-class form validation behaviour   
        # Llamar al comportamiento de validación del formulario de la superclase
        return super(BlogCommentCreate, self).form_valid(form)

    def get_success_url(self): 
        """
        After posting comment return to associated blog.
        Después de publicar el comentario, volver al blog asociado.
        """
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk'],})