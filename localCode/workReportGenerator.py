from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.shared import Inches, Pt
from docx.enum.text import  WD_PARAGRAPH_ALIGNMENT


def generateDocument():
    # создаём документ
    document = Document()
    # задаём отступы
    document.sections[0].top_margin = 200000
    document.sections[0].left_margin = 600000
    document.sections[0].right_margin = 200000
    # создаём таблицу
    table = document.add_table(rows=20, cols=6)
    table.style = 'TableGrid'
    #  table.alignment = WD_TABLE_ALIGNMENT.CENTER

    cell = table.cell(0, 0).merge(table.cell(0, 1)).merge(table.cell(0, 2)).merge(table.cell(0, 3))
    cell.text = 'Сменный наряд ШАВ-124-16.01.2017'
    p = cell.paragraphs[0]
    p.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p.font.size = Pt(20)
    p.font.bold = True

    table.cell(0, 4).merge(table.cell(0, 5))

    #table.cell(0, 0).text = 'asd'

    document.add_page_break()
    return document


if __name__ == "__main__":
    document = generateDocument()
    document.save('out/demo.docx')


# document.add_heading('Document Title', 0)


# p = document.add_paragraph('A plain paragraph having some ')
# p.add_run('bold').bold = True
# p.add_run(' and some ')
# p.add_run('italic.').italic = True

# document.add_heading('Heading, level 1', level=1)
# document.add_paragraph('Intense quote', style='IntenseQuote')

# document.add_paragraph(
#  'first item in unordered list', style='ListBullet'
# )
# document.add_paragraph(
#   'first item in ordered list', style='ListNumber'
# )

# document.add_picture('in/img.jpg', width=Inches(1.25))



# for item in recordset:
#    row_cells = table.add_row().cells
#    row_cells[0].text = str(item.qty)
#    row_cells[1].text = str(item.id)
#    row_cells[2].text = item.desc
