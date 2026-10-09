"""Six-page, blue-themed lab report. Preview figures are explicitly labelled."""
from pathlib import Path
import json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from generate_evaluation_data import ROOT

NAVY=colors.HexColor('#09203a');BLUE=colors.HexColor('#175997');PALE=colors.HexColor('#eaf3fc');MUTED=colors.HexColor('#41576d')
def main():
    font=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    bold=font.with_name('DejaVuSans-Bold.ttf')
    if font.exists():
        pdfmetrics.registerFont(TTFont('Body',str(font)));pdfmetrics.registerFont(TTFont('BodyBold',str(bold)))
        pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='Body',boldItalic='BodyBold')
    else:
        pdfmetrics.registerFontFamily('Body',normal='Helvetica',bold='Helvetica-Bold',italic='Helvetica-Oblique',boldItalic='Helvetica-BoldOblique')
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='LabTitle',fontName='BodyBold',fontSize=26,leading=32,textColor=NAVY,spaceAfter=18))
    styles.add(ParagraphStyle(name='LabH1',fontName='BodyBold',fontSize=18,leading=23,textColor=BLUE,spaceAfter=14))
    styles.add(ParagraphStyle(name='LabH2',fontName='BodyBold',fontSize=11.8,leading=16,textColor=NAVY,spaceBefore=12,spaceAfter=7))
    styles.add(ParagraphStyle(name='LabBody',fontName='Body',fontSize=9.8,leading=15,textColor=NAVY,spaceAfter=9))
    styles.add(ParagraphStyle(name='LabSmall',fontName='Body',fontSize=8.3,leading=12,textColor=MUTED,spaceAfter=7))
    styles.add(ParagraphStyle(name='LabCell',fontName='Body',fontSize=8.2,leading=11.5,textColor=NAVY))
    styles.add(ParagraphStyle(name='LabWhite',fontName='BodyBold',fontSize=8.5,leading=12,textColor=colors.white))
    story=[]
    def p(text,style='LabBody'):story.append(Paragraph(text,styles[style]))
    def h(text):p(text,'LabH2')
    def table(rows,widths):
        data=[[Paragraph(str(v),styles['LabWhite'] if i==0 else styles['LabCell']) for v in row] for i,row in enumerate(rows)]
        t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),BLUE),('ROWBACKGROUNDS',(0,1),(-1,-1),[PALE,colors.white]),
            ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
            ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
            ('LINEBELOW',(0,0),(-1,0),.7,BLUE)]));story.append(t);story.append(Spacer(1,10))
    def page(title):story.append(PageBreak());p(title,'LabH1')
    p('EVALUATION DASHBOARD LAB','LabH1');p('From evaluation records<br/>to stakeholder decisions','LabTitle')
    p('<b>Walid Barakat</b> | i@work | 8 October 2026')
    p('Tableau solution route with an offline browser preview and optional judge-agreement extension.')
    h('Goal')
    p('Explain where evaluation quality varies across categories and candidate versions, and let a manager inspect the results through clear filters. Technical preparation and audit evidence stay in the notebook and documentation.')
    h('Data choice')
    p('Option B: 9,000 synthetic evaluation rows covering five categories, four generic candidates and 90 days. The fixed window is 10 July to 7 October 2026. There are 2,250 distinct examples, each evaluated for all four candidates. Seed 42 makes the data reproducible.')
    table([['Default metric','Simulated result'],['Average rubric score','55.26 / 100'],['Scores at or above illustrative target 80','15.50%'],['Weakest / strongest category','Reasoning / instruction following'],['Judge agreement within 10 points','61.96%'],['Average judge score gap','9.03 points']],[257,250])
    h('Readiness and limits')
    p('<b>Prepared and checked:</b> CSVs, native workbook files, HTML preview, Python notebook, labelled preview images, reflection, README and submission guide. Local data, JavaScript logic and Tableau XML/packaging checks passed.')
    p('<b>Before submission:</b> open and verify the workbooks in Tableau, test native filters, save genuine dashboard screenshots, and upload the dedicated lab repository to GitHub. No native screenshot or published repository is claimed.')
    p('All scores and candidate differences are simulated. They do not establish commercial model quality, measured savings or performance of the EU tender agent.','LabSmall')
    page('1. Main dashboard preview')
    story.append(Image(str(ROOT/'dashboard_preview.png'),width=507,height=462))
    p('Figure 1. Preview render generated from the exact dashboard chart code. This is not a screenshot from Tableau Desktop.','LabSmall')
    h('Reading the view')
    p('The histogram shows how many evaluations fall in each score band. The category box view shows the middle half of scores, median and minimum/maximum. The sorted bars expose improvement priorities. The candidate grid checks whether a weakness is common across versions.')
    p('Use model, category and date controls in the HTML file. Clicking a category chart applies a filter, and a candidate cell selects both candidate and category. Reset restores the full set. CSV export downloads only the selected rows.')
    p('Native Tableau uses a category-by-score-range heatmap for the distribution sheet; the HTML preview uses a box plot. Both complement the separate ranked comparison.','LabSmall')
    page('2. Data preparation and chart solution')
    h('Steps 1-3: prepare data')
    p('Generate records using the included script, keep raw and clean CSVs, verify numeric scores and canonical dates, and document Option B in data_source.md. No rows were removed: the generator produces valid complete records. Keep genuine 0 and 100 values.')
    table([['Validation','Evidence'],['9,000 unique evaluation IDs; no missing critical values','docs/data_quality_report.json'],['Five categories, four candidates, 90 dates','450 rows per category/candidate combination'],['Raw score and judge ranges','All score fields remain within 0-100'],['Repeatability and error cases','10 Python tests, including missing scores, invalid dates and duplicate IDs']],[270,237])
    h('Steps 4-7: connect and create charts')
    table([['Native Tableau worksheet','Fields / aggregation'],['Score Distribution','score_range; SUM(Row Count)'],['Scores by Category','category x score_range; SUM(Row Count) on colour and label'],['Category Comparison','category vs AVG(score), descending order'],['Candidate Comparison','category x model_version; AVG(score)'],['Summary cards','AVG(score), SUM(Row Count), AVG(meets_target)']],[226,281])
    p('Counts are row counts, not summed evaluation IDs. Average quality is a row-weighted mean. Score ranges are lower-inclusive and upper-exclusive, except 90-100 includes 100. Target rate is the mean of a 0/1 indicator for score at least 80.')
    h('Steps 8-10: communication and interaction')
    p('Use model/category/date filters across every chart and card. Keep score definitions, record counts, clear titles and the synthetic-data label visible. Use category cross-filtering and concise next-action language. Generation assumptions, data checks and statistical details belong in the notebook.')
    p('The native comparison reference line averages displayed category means. It equals the row-weighted mean in this balanced sample; the preview always uses the selected-row mean. Check this distinction when replacing the sample with uneven real data.','LabSmall')
    page('3. Optional judge-agreement solution')
    story.append(Image(str(ROOT/'judge_agreement_preview.png'),width=507,height=449))
    p('Figure 2. Judge dashboard preview render, not a native Tableau screenshot. Every selected rating pair is plotted.','LabSmall')
    h('Interpretation')
    p('Agreement means an absolute score gap of 10 points or less. The mean agreement is 61.96%, mean gap is 9.03 points, and 3,424 cases exceed the tolerance. Agreement is not proof of correct ratings: two judges can share a mistake.')
    p('The bars show which categories have more consistent ratings. The gap histogram shows disagreement sizes. The scatter makes rating differences visible. In the preview, the diagonal is equality and dashed lines represent the 10-point tolerance. The native workbook also includes an association trend line.')
    p('Compute agreement from the exported rounded judge scores. A difference of exactly 10 counts as agreement even though its histogram bin starts at 10. Review large gaps against a human-approved rubric before drawing conclusions.','LabSmall')
    page('4. Verification and requirements status')
    table([['Requirement','Current status / next evidence'],['Clean evaluation data and source note','Delivered and validated; synthetic Option B disclosed'],['At least three charts and filters','Native XML prepared; preview chart logic tested'],['Stakeholder-friendly communication','Titles, scale, sample count, synthetic label and interpretation included'],['Final native dashboard file','Main and optional TWBX delivered; actual Tableau opening/filter checks pending'],['Dashboard screenshot','Labelled preview renders supplied; real Tableau screenshots pending'],['Reflection and README','Delivered; personalise the suggested reflection after Tableau checks'],['GitHub-only submission','Dedicated-folder package prepared; repository upload and actual URL pending']],[209,298])
    h('Evidence completed')
    p('Ten Python tests passed. Twelve JavaScript logic checks passed, including combined filters, chart clicks, reset, empty results, CSV export and judge agreement. JavaScript ran with DOM test doubles and a canvas renderer, so browser end-to-end behaviour is not claimed. The notebook contains eight executed Python cells, run through a local cell runner rather than a Jupyter kernel.')
    p('Two TWB sources and two packaged TWBX files passed structural checks using Tableau\'s official 2026.2 schema, workbook-reference checks, ZIP integrity and embedded-CSV checks. The published schema imports two namespaces without locations; validation supplies namespace declarations for those imports without changing the main workbook structure.')
    h('Why native verification is still necessary')
    p('Tableau states that schema validation does not guarantee that a workbook opens in the product. Tableau Desktop was unavailable here. The package therefore distinguishes prepared files from confirmed native rendering and includes a manual rebuild recipe if the generated workbook needs correction.')
    h('Known interaction counts')
    p('All data: 9,000. Candidate A: 2,250. Reasoning: 1,800. Candidate A plus reasoning: 450. The same selection on 7 October only: 5. Every card and chart should follow these selections, and reset should return to 9,000.')
    page('5. Submission, reflection and sources')
    h('Finish and submit')
    p('1. Open the main TWBX in Tableau Desktop 2026.2 or later and verify the CSV connection.<br/>2. Apply all filters to all relevant worksheets, enable category cross-filtering, and check the known counts.<br/>3. Re-save the verified workbook and capture dashboard_screenshot.png from Tableau.<br/>4. Repeat for the optional judge dashboard and capture judge_agreement_screenshot.png.<br/>5. Review the reflection, update status evidence, upload only this lab to a dedicated GitHub repository and submit its actual URL.')
    h('Suggested reflection')
    p('I designed the dashboard around a manager\'s questions: where scores are weak, whether the pattern changes by candidate, and which examples deserve review. Clear definitions, sample counts and simple filters support those decisions. I kept code and validation details outside the communication layer.')
    p('The generated data limit what I can conclude. A real follow-up would use held-out evaluations from my EU tender agent, the same examples across candidates, and a documented human-reviewed rubric. I would inspect low-score reasoning examples, make one targeted change and track quality, cost and review time before claiming business impact.')
    h('Package map')
    p('README.md maps every deliverable. The notebook documents calculations. data/ contains CSVs and summaries. scripts/ regenerates data and dashboards. tests/ contains local checks. docs/ holds the Tableau guide, requirement matrix, interpretation and GitHub instructions. Preview images are labelled and kept separate from required native screenshots.')
    h('Primary references')
    links=[('Assignment','Uploaded LAB | Evaluation Dashboard Lab(1).pdf: steps 1-11, deliverables and optional extension',None),
      ('Tableau packaged workbooks','Local data inside TWBX','https://help.tableau.com/current/pro/desktop/en-us/save_savework_packagedworkbooks.htm'),
      ('Tableau filters','Interactive controls and worksheet scope','https://help.tableau.com/current/pro/desktop/en-us/filtering.htm'),
      ('Tableau filter actions','Selection-based dashboard filtering','https://help.tableau.com/current/pro/desktop/en-us/actions_filter.htm'),
      ('Official Tableau document schemas','2026.2 structure and limits of syntactic validation','https://github.com/tableau/tableau-document-schemas')]
    for name,description,url in links:
        p(f'<b>{name}:</b> {description}'+(f'<br/><link href="{url}" color="#175997">{url}</link>' if url else ''),'LabSmall')
    p('All numerical findings were calculated from the included synthetic CSVs. No unsupported score, real-vendor ranking, fabricated GitHub URL or measured business saving is used.','LabSmall')
    out=ROOT/'Evaluation_Dashboard_Lab_Solution.pdf'
    def decorate(canvas,doc):
        canvas.setFillColor(NAVY);canvas.rect(0,A4[1]-15,A4[0],15,fill=1,stroke=0)
        canvas.setFont('Body',8);canvas.setFillColor(MUTED)
        canvas.drawString(44,23,'Walid Barakat | Evaluation Dashboard Lab | Synthetic-data solution')
        canvas.drawRightString(A4[0]-44,23,str(doc.page))
    doc=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=44,leftMargin=44,topMargin=42,bottomMargin=40,
        title='Evaluation Dashboard Lab Solution',author='Walid Barakat')
    doc.build(story,onFirstPage=decorate,onLaterPages=decorate)
    print(out.name)

if __name__=='__main__':main()
