import BD_SQL
import GOOGLE_SHEETS

def atualizar_relatorio():
    lista= BD_SQL.main(selecionar_colocado= 1)
    GOOGLE_SHEETS.main(lista)
    
atualizar_relatorio()

