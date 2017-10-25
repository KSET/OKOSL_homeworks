from django import forms


class MovieForm(forms.Form):
    # categories = ['Comedy', 'Animation', 'Music', 'Foreign',
    #               'Documentary', 'Classics', 'Action', 'New',
    #               'Sports', 'Family', 'Children', 'Travel',
    #               'Horror', 'Games', 'Drama', 'Sci-Fi']

    title = forms.CharField(label='Title', max_length=100, initial='Movie title')
    # category = forms.MultipleChoiceField(label='Category: ', choices=categories)
    category = forms.CharField(label='Category', max_length=100, initial='Movie category')
    summary = forms.CharField(label='Summary', max_length=100, initial='Movie summary')
    description = forms.CharField(label='Description', max_length=500, initial='Movie description')


class SearchForm(forms.Form):
    # categories = ['Comedy', 'Animation', 'Music', 'Foreign',
    #               'Documentary', 'Classics', 'Action', 'New',
    #               'Sports', 'Family', 'Children', 'Travel',
    #               'Horror', 'Games', 'Drama', 'Sci-Fi']

    title = forms.CharField(label='Title', max_length=100, initial='Movie title', required=False)
    # category = forms.MultipleChoiceField(label='Category: ', choices=categories)
    category = forms.CharField(label='Category', max_length=100, initial='Movie category', required=False)
    summary = forms.CharField(label='Summary', max_length=100, initial='Movie summary', required=False)
    description = forms.CharField(label='Description', max_length=500, initial='Movie description', required=False)
