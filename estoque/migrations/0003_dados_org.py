from django.db import migrations


def org_padrao(apps, schema_editor):
    Organizacao = apps.get_model('core', 'Organizacao')

    organizacao, _ = Organizacao.objects.get_or_create(
        nome='Organização padrão'
    )

    for nome_model in [
        'Fornecedor',
        'Produto',
        'Deposito',
        'Movimentacao'
    ]:
        Model = apps.get_model('estoque', nome_model)

        Model.objects.filter(
            organizacao__isnull=True
        ).update(organizacao=organizacao)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('estoque', '0002_organizacao_nula'),
    ]

    operations = [
        migrations.RunPython(
            org_padrao,
            migrations.RunPython.noop
        ),
    ]
