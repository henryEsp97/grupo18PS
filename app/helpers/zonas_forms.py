from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields import SelectField


class ImportForm(FlaskForm):
    file = FileField('Buscar archivo', validators=[
        FileRequired(),
        FileAllowed(['csv'], 'Por favor, seleccione un archivo .csv')
    ])

class UpdateForm(FlaskForm):
    estado = SelectField(u'Estado', choices=[('1', 'Publicado'), ('0', 'Despublicado')])
    color = SelectField(u'Color', choices=[('#34f409', 'Verde'), ('#fb3715', 'Rojo')])