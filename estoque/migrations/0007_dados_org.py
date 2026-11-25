from django.db import migrations


def atribuir_org_padrao(apps, schema_editor):
    Organizacao = apps.get_model("core", "Organizacao")
    org, _ = Organizacao.objects.get_or_create(nome="Organização padrão")

    for model_name in ["Fornecedor", "Produto", "Deposito", "Movimentacao"]:
        Model = apps.get_model("estoque", model_name)
        Model.objects.filter(organizacao__isnull=True).update(organizacao=org)


class Migration(migrations.Migration):
    dependencies = [
        ("estoque", "0006_alter_deposito_organizacao_and_more"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(atribuir_org_padrao, migrations.RunPython.noop),
    ]