# coding: utf-8
"""
    Name:        views.py
    Purpose:
    Author:      GPS-PC08
    Created:     28/03/2023
    com implementação de classe listview herdada classificada asc ou desc por qq campo (class TemaListViewSorted)
    com implementação de paginação em todas as classes
"""
##-----------------------------IMPORTS------------------------------------------
from django.shortcuts import render

from .models import Coment, Tema, TemaComent
from django.db.models import Count
from django.views import generic

from eletronlab import settings
#
from django.contrib.auth.mixins import LoginRequiredMixin

import locale

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

##-----------------------------GLOBALS------------------------------------------
paginacao=15




##--------------------FUNCTIONS AND CLASSES-------------------------------------
# ##################################################################################################################################
def home(request):
    #verifica a fonte de dados
    a=settings.DATABASES['default']['HOST']
    if 'mysql.uhserver.com' in a:
        db_server='UOL Host'
    if 'localhost' in a:
        db_server='localhost'
    db_db=settings.DATABASES['default']['NAME']

    """View function for home page of site."""

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1


    # Generate counts of some of the main objects
    num_temas = Tema.objects.all().count()
    num_temacoments = TemaComent.objects.all().count()

    # temas ja estudados (todos - aqueles cujo campo ordem = NULL
    num_temas_estudados = num_temas-Tema.objects.filter(ordem__exact=None).count()

    # The 'all()' is implied by default.
    tmp1=Coment.objects.aggregate(Count('assunto', distinct=True))
    num_assuntos = tmp1['assunto__count']

    percentual_temas_estudados = "{0:,.1f}%".format((num_temas_estudados/num_temas)*100)

    tmp2=Coment.objects.filter(assunto__exact="ci").aggregate(Count('detalhe', distinct=True))
    num_cis = tmp2['detalhe__count']

    context = {
        'num_temas': num_temas,
        'num_temacoments': num_temacoments,
        'num_temas_estudados': num_temas_estudados,
        'num_assuntos': num_assuntos,
        'percentual_temas_estudados': percentual_temas_estudados,
        'num_cis': num_cis,
        'num_visits': num_visits,
        'db_server': db_server,
        'db_db': db_db,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'home.html', context=context)


# ##################################################################################################################################
class TemaListViewSorted(generic.ListView):
    model = Tema
    template_name = 'estudoa/tema_list.html'
    paginate_by = paginacao

    sort_url='1a'
    sort_por = ''

    #mapemento das colunas/campos da tabela Tema (sort,field,sorted
    sort_colunas = [
            ['1a', 'codtema', '0'],
            ['2a', 'semana', '0'],
            ['3a', 'ordem', '0'],
            ['4a', 'titulo', '0'],
            ['5a', 'categoria', '0'],
            ['6a', 'pagina', '0'],
    ]


    filtro_url=''
    filtro_sem=''
    filtro_cat=''
    filtro_page=''

    #Lista exclusiva de categorias criando uma lista exclusiva a partir da função set do python
    filtro_lst_cat=list(set(Tema.objects.values_list("categoria")))
    for i in range(len(filtro_lst_cat)):
        filtro_lst_cat[i]=filtro_lst_cat[i][0]
    #note que para que os caracteres utf-8 sejam considerados há qe se usar o módulo locale
    locale.setlocale(locale.LC_ALL, '')
    filtro_lst_cat=sorted(filtro_lst_cat,key=locale.strxfrm)
    filtro_lst_cat.insert(0,"")

    # fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff----get_queryset
    def get_queryset(self):
    #              CLASSIFICAÇÃO CRESCENTE OU DECRESCENTE            ******************************************************************
        #Define ou pega o parâmetro da session 'col_classif'. Usa-se session para não perder as escolhas do usuário
        col_classif = self.request.session.get('col_classif', '1a')
        # Captura do parâmetro col da URL da coluna clasificada pelo usuário, contendo o número da coluna e a ordem, asc ou desc
        self.sort_url=self.request.GET.get('col',col_classif) #caso não encontre retorna o padrão, col_classif
        #Redefine o parâmetro da session 'col_classif' como o parâmetro passado pela url, parâmetro 'col'
        self.request.session['col_classif'] = self.sort_url

        # pega/converte em número a coluna (base 0) passada pela parâmetro col da url da coluna escolhida pelo usuário
        tmp=int(self.sort_url[0])-1

        #reseta a classificação para nenhuma
        for i in range(6):
            self.sort_colunas[i][2]='0'

        #Verifica se a classificação é ascendente (a) ou descendente (d)
        if self.sort_url[1]=='a':
            self.sort_por = self.sort_colunas[tmp][1]
            #atualizar as variáves de contexto
            self.sort_colunas[tmp][0]= f"{tmp+1}d"
            self.sort_colunas[tmp][2]='1'
        elif self.sort_url[1]=='d':
            self.sort_por = '-' + self.sort_colunas[tmp][1]
            #atualizar as variáves de contexto
            self.sort_colunas[tmp][0]= f"{tmp+1}a"
            self.sort_colunas[tmp][2]='1'

        #              FILTRAGEM POR SEMANA OU CATEGORIA               **************************************************************
        #Define ou pega o parâmetro da session 'filtro_semana'. Usa-se session para não perder as escolhas do usuário
        filtro_semana = self.request.session.get('filtro_semana', '')
        # Captura os parâmetros para filtragem contidos na URL quando se clica em "filtrar"
        self.filtro_sem=self.request.GET.get('semana',filtro_semana) #caso não encontre retorna o padrão, filtro_semana
        #Redefine o parâmetro da session 'filtro_semana' como o parâmetro passado pela url, parâmetro 'semana'
        self.request.session['filtro_semana'] = self.filtro_sem
        #torna o valor do filtro de semana um valor inteiro
        if self.filtro_sem != '':
            self.filtro_sem=int(self.filtro_sem)

        #Define ou pega o parâmetro da session 'filtro_categoria'. Usa-se session para não perder as escolhas do usuário
        filtro_categoria = self.request.session.get('filtro_categoria', '')
        self.filtro_cat=self.request.GET.get('categoria',filtro_categoria) #caso não encontre retorna o padrão, filtro_categoria
        #Redefine o parâmetro da session 'filtro_categoria' como o parâmetro passado pela url, parâmetro 'categoria'
        self.request.session['filtro_categoria'] = self.filtro_cat

        #Verifica e configura o tipo de filtragem e classificação escolhida pelo usuário
        if self.filtro_sem != '':
            queryset=Tema.objects.filter(semana__exact=int(self.filtro_sem)).order_by(self.sort_por)
            self.filtro_url=f"&semana={self.filtro_sem}"
        elif self.filtro_cat !='':
            queryset=Tema.objects.filter(categoria__exact=f'{self.filtro_cat}').order_by(self.sort_por)
            self.filtro_url=f"&categoria={self.filtro_cat}"
        else:
            queryset=Tema.objects.all().order_by(self.sort_por)
        return queryset

    # fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff----get_context_data
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        # Create any data and add it to the context
        context['c0'] = f'{self.sort_colunas[0][0]}{self.sort_colunas[0][2]}'
        context['c1'] = f'{self.sort_colunas[1][0]}{self.sort_colunas[1][2]}'
        context['c2'] = f'{self.sort_colunas[2][0]}{self.sort_colunas[2][2]}'
        context['c3'] = f'{self.sort_colunas[3][0]}{self.sort_colunas[3][2]}'
        context['c4'] = f'{self.sort_colunas[4][0]}{self.sort_colunas[4][2]}'
        context['c5'] = f'{self.sort_colunas[5][0]}{self.sort_colunas[5][2]}'
        context['sort_url'] = self.sort_url
        context['filtro_url'] = self.filtro_url
        context['filtro_sem'] = self.filtro_sem
        context['filtro_cat'] = self.filtro_cat
        context['filtro_lst_cat'] = self.filtro_lst_cat
        context['filtro_page'] = self.filtro_page
        return context

# ##################################################################################################################################
class TemaDetailView(generic.DetailView):
    template_name = 'estudoa/tema_detail.html'  # Specify your own template name/location
    model = Tema

# ##################################################################################################################################
class ComentListView(generic.ListView):
    model = Coment
    template_name = 'estudoa/coment_list.html'  # Specify your own template name/location
    paginate_by = paginacao

# ##################################################################################################################################
class ComentDetailView(generic.DetailView):
    model = Coment
    template_name = 'estudoa/coment_detail.html'  # Specify your own template name/location

# ##################################################################################################################################
class TemaComentListView(generic.ListView):
    model = TemaComent
    template_name = 'estudoa/temacoment_list.html'  # Specify your own template name/location
    paginate_by = paginacao

# ##################################################################################################################################
class TemaComentDetailView(generic.DetailView):
    model = TemaComent
    template_name = 'estudoa/temacoment_detail.html'  # Specify your own template name/location

# ##################################################################################################################################
class TemaUpdate(UpdateView):
    model = Tema
    fields = ['semana', 'ordem', 'titulo', 'categoria', 'pagina']



class ComentCreate(CreateView):
    model = Coment
    fields = ['assunto', 'detalhe']

class ComentUpdate(UpdateView):
    model = Coment
    fields = ['assunto', 'detalhe']

class ComentDelete(DeleteView):
    model = Coment
    success_url = reverse_lazy('coments')


class TemaComentCreate(CreateView):
    model = TemaComent
    fields = ['tema', 'coment']
    success_url = reverse_lazy('tema-detail')

    # fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff----get_success_url
    def get_success_url(self):
         return reverse('tema-detail', kwargs={'pk': self.request.GET.get('tema',1)})

    # fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff----get_initial
    def get_initial(self):
        return {
            'tema':self.request.GET.get('tema',1),
        }


class TemaComentDelete(DeleteView):
    model = TemaComent
    success_url = reverse_lazy('temacoments')