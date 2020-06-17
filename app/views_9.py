from flask import render_template, flash, redirect, url_for, Response
from app import app
from app.forms import LoginForm, HspotADDForm, HspotREMForm, SetradiusForm, SetminimumroutelengthForm, parametersForm, setthresholdNumForm
import math

radius = str(79000)
tnum = str(0.5)
min_r_len = str(100)

@app.route('/')
@app.route('/index_9')
def index_9():
    return render_template('index_9.html', title='Home')



@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = LoginForm()
    if form.validate_on_submit():
        '''if (form.username.data=="Shivam" and form.password.data=="JaiShriRam"):
            return render_template('admin_home.html', title= 'Admin Home')
        else:
            return redirect(url_for('admin'))'''
        return render_template('admin_home.html', title= 'Admin Home')
    return render_template('admin.html',  title='Sign In', form=form)



@app.route('/visitor_home')
def visitor_home():    
    return render_template('visitor_home.html',  title='Visitor Home')



@app.route('/ahotspots', methods=['GET', 'POST'])
def ahotspots():
    form = HspotADDForm()
    if form.validate_on_submit():
        
        
        with open('Hotspots.txt', 'a') as f:
            f.write('\n'+form.hspot.data) 
        
        rem_emp_lines()
        
        string = form.hspot.data+' is successfully added to hotspot list, however database has not been updated yet.'
        string2 = 'Please click on update database button to update the database'
        return render_template('ahotspots.html',  title='Add a hotspot', string=string,form=form,string2=string2)
    return render_template('ahotspots.html',  title='Add a hotspot', form=form)




@app.route('/rhotspots', methods=['GET', 'POST'])
def rhotspots():
    form = HspotREMForm()
    if form.validate_on_submit():
       
        
        
        with open("Hotspots.txt", "r") as f:
            lines = f.readlines()
        with open("Hotspots.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != form.hspotr.data:
                    f.write(line)
        rem_emp_lines()
        string = form.hspot.data+' is successfully removed from the hotspot list, however database has not been updated yet. Please click on update database button to update the database'
        return render_template('rhotspots.html',  title='Remove a hotspot', string=string,form=form)  
    return render_template('rhotspots.html',  title='Remove a hotspot',form = form)



@app.route('/radius_of_hotspot', methods=['GET', 'POST'])
def radius_of_hotspot():
    global radius
    form = SetradiusForm()
    if form.validate_on_submit():
        
        radius = form.setr.data
        string = 'Radius of hotspots is set to '+form.setr.data+' meters, however database has not been updated yet. Please click on update database button to update the database'
        return render_template('radius_of_hotspot.html',  title='Set the radius of hotspots', string=string,form=form)
    return render_template('radius_of_hotspot.html',  title='Set the radius of hotspots', form=form)



@app.route('/threshold_num', methods=['GET', 'POST'])
def threshold_num():
    global tnum
    form = setthresholdNumForm()
    if form.validate_on_submit():
        
        tnum = form.setnum.data
        string = 'Threshold number for considering station to be operational is set to '+form.setnum.data+' meters, however database has not been updated yet. Please click on update database button to update the database'
        return render_template('threshold_num.html',  title='Set the threshold number', string=string,form=form)
    return render_template('threshold_num.html',  title='Set the threshold number', form=form)        



@app.route('/length_of_route', methods=['GET', 'POST'])
def length_of_route():
    global min_r_len
    form = SetminimumroutelengthForm()
    if form.validate_on_submit():
        
        min_r_len = form.setmrl.data
        string = 'Minimun length of the train route is set to '+form.setnum.data+' kilometers, however database has not been updated yet. Please click on update database button to update the database'
        return render_template('length_of_route.html',  title='Set the length of route', string=string,form=form)
    return render_template('length_of_route.html',  title='Set the length of route', form=form)


@app.route('/update_db')
def update_db():
            calc_dist_from_hotspots()
            numbering()
            working_list()
            making_new_routes()
            calc_length_of_new_routes()
            only_minimun_length_routes() 
            flash('Database is updated successfully. You can use the visitor section in order to see the updated results.')            
            return redirect(url_for('admin'))




@app.route('/trains_list')
def trains_list():
    f = open('Re_reversed_new_routes_lengths.txt','r')
    
    return Response(f.read(), mimetype='text/plain')



@app.route('/hotspots_list')
def hotspots_list():
    f = open('Hotspots.txt','r')

    return Response(f.read(), mimetype='text/plain')





###################################################################################################

######################################################################################################################################









def calc_dist_from_hotspots():
        f = open('result_Distance_Between_Every_Station_CodeVersion.txt','r')
        g = open('1_Distances_from_the_Hotspots.txt','w')
        h = open('Hotspots.txt','r')


        l=[]

        for z in h:
            t = z.strip("\n")
            l.append(t)    

        for x in f:
            t = x.split(",")
            if t[0] in l:
                g.write(t[0]+" "+t[3]+" "+t[6])
        #################################################      
        f = open('result_Distance_Between_Every_Station_2_from_1674_CodeVersion.txt','r')
        g = open('2_Distances_from_the_Hotspots.txt','w')
        h = open('Hotspots.txt','r')

        #l = ['LTT','PUNE','TNA','PLG','NK','NGP','ROHA','AWB','PLO','SUR','ANG','STR','AK','SLI','DHI','MKU','AMI','JL','NDB','KOP','LUR','RN','HNL','UMD','J','CD','WHM','SNDD','PBN','NED','G','BID','ADI','ST','BRC','ANND','RJT','BVC','BH','PNU','GNC','BTD','PTN','AVRD','PPD','BTD','GDA','MSH','MHD','BL','DHD','PBR','NVS','SMNH','NWU','SUNR','MVI','JAM','NDLS','DLI','DSA','DEE','NZM','DSJ','JP','JU','KOTA','AII','BHTK','NGO','BTE','BOG','JJN','JLWC','BKN','JSM','BHL','DO','CUR','HMH','SWM','AWR','UDZ','SIKR','DHO','SMBJ','PBH','PMY','BME','MVJ','COR','INDB','BPL','UJN','KNW','JBP','HBD','SCI','DDE','DWX','BHS','RTM','MRA','MKC','MDS','SFY','SGO','CWA','GWL','TKMG','SVPI','SDL','BZU','AGC','CNB','LJN','SRE','CHL','MB','FZD','MUT','GZB','BSC','RBL','BSB','BJO','SMQL','HPU','AMRO','BST','ALJN','MHH','RMU','SPC','MOZ','BEM','BPM','MTJ','PHD','AMH','PBH','KJN','BE','GH','GCT','MNQ','JNU','HTC','SLN','PBE','MZP','KSJ','BNDA','ANVT','ORAI','HRI','ETW','ON','MAU','JHS','GKP','GD','BOY','BBK','BLP','AY','MAS','CBE','TUP','DG','MDU','ED','TEN','NMKL','CGL','TRL','TJ','VM','TPJ','NGT','KRR','MCN','TSI','VPT','SA','TVR','CUPJ','VLR','TPT','CJ','CAPE','RMD','SVGA','TNM','ALU','PDKT','DPJ','KRNT','GNT','KCC','NLR','CTO','HX','SKM','GVN','ATP','VSKP','CHE','HYB','MRGA','NZB','GWD','VKB','WL','MJF','ADB','KRMR','NLDA','KMC','MBNR','KMT','SKP','ASAF','BDCR','ZN','LPJL','PDPL','KRNT','WDR','MCI','MABD','KOAA','HWH','MDN','BWN','DJ','JPG','DJ','MBB','SBC','MYS','BGM','BJP','KLBG','BGK','MYA','BIDR','BAY','DWR','GDG','UD','TK','DVG','CTA','KGQ','CAN','CLT','ETM','ERS','AAM','KTYM','CNGR','TVC','QLN','TCR','PGT','ALLP','NIL','MGR','PNBE','NLD','JPL','SV','BXR','KTQ','GOPG','KRS','BGS','AUBR','GAYA','MBI','BMKI','BGP','CPR','NWD','LKR','JHD','GRL','BAKA','PRNA','DMH','DBG','JUC','SASN','PTA','PTK','LDH','ASR','MSZ','HSX','KXH','MOGA','SAG','RPAR','FDK','FGSB','BNN','MKS','GSP','FZR','AST','GGN','FDB','PWL','SNP','CDG','UMB','PNP','KUN','SSA','ROK','HSR','YJUD','BNW','KKDE','KLE','JHJ','CKD','KUR','JJKR','BHC','BLS','BEH','KNPR','JNRD','PURI','KRPU','DNKL','CTC','RNC','BKSC','DTO','HZD','GHQ','BANO','DHN','DGHR','KQR','JMT','GRD','DDN','KGM','HW','HLDD','KTW','CDG','UHL','MDPB','HAR','KRBA','R','RJN','DURG','BSP','JTTN','KYQ','GLPT','DBB','NLV','CPK','SCL','LMP','GLGT','PDY','MAHE','KRMI','CNO']

        l=[]

        for z in h:
            t = z.strip("\n")
            l.append(t)    

        for x in f:
            t = x.split(",")
            if t[0] in l:
                g.write(t[0]+" "+t[3]+" "+t[6])
    

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

def numbering():
        dist = radius
        print(dist)
        f = open('1_Distances_from_the_Hotspots.txt','r')
        h = open('Hotspots.txt','r')
        
        #l = ['LTT','PUNE','TNA','PLG','NK','NGP','ROHA','AWB','PLO','SUR','ANG','STR','AK','SLI','DHI','MKU','AMI','JL','NDB','KOP','LUR','RN','HNL','UMD','J','CD','WHM','SNDD','PBN','NED','G','BID','ADI','ST','BRC','ANND','RJT','BVC','BH','PNU','GNC','BTD','PTN','AVRD','PPD','BTD','GDA','MSH','MHD','BL','DHD','PBR','NVS','SMNH','NWU','SUNR','MVI','JAM','NDLS','DLI','DSA','DEE','NZM','DSJ','JP','JU','KOTA','AII','BHTK','NGO','BTE','BOG','JJN','JLWC','BKN','JSM','BHL','DO','CUR','HMH','SWM','AWR','UDZ','SIKR','DHO','SMBJ','PBH','PMY','BME','MVJ','COR','INDB','BPL','UJN','KNW','JBP','HBD','SCI','DDE','DWX','BHS','RTM','MRA','MKC','MDS','SFY','SGO','CWA','GWL','TKMG','SVPI','SDL','BZU','AGC','CNB','LJN','SRE','CHL','MB','FZD','MUT','GZB','BSC','RBL','BSB','BJO','SMQL','HPU','AMRO','BST','ALJN','MHH','RMU','SPC','MOZ','BEM','BPM','MTJ','PHD','AMH','PBH','KJN','BE','GH','GCT','MNQ','JNU','HTC','SLN','PBE','MZP','KSJ','BNDA','ANVT','ORAI','HRI','ETW','ON','MAU','JHS','GKP','GD','BOY','BBK','BLP','AY','MAS','CBE','TUP','DG','MDU','ED','TEN','NMKL','CGL','TRL','TJ','VM','TPJ','NGT','KRR','MCN','TSI','VPT','SA','TVR','CUPJ','VLR','TPT','CJ','CAPE','RMD','SVGA','TNM','ALU','PDKT','DPJ','KRNT','GNT','KCC','NLR','CTO','HX','SKM','GVN','ATP','VSKP','CHE','HYB','MRGA','NZB','GWD','VKB','WL','MJF','ADB','KRMR','NLDA','KMC','MBNR','KMT','SKP','ASAF','BDCR','ZN','LPJL','PDPL','KRNT','WDR','MCI','MABD','KOAA','HWH','MDN','BWN','DJ','JPG','DJ','MBB','SBC','MYS','BGM','BJP','KLBG','BGK','MYA','BIDR','BAY','DWR','GDG','UD','TK','DVG','CTA','KGQ','CAN','CLT','ETM','ERS','AAM','KTYM','CNGR','TVC','QLN','TCR','PGT','ALLP','NIL','MGR','PNBE','NLD','JPL','SV','BXR','KTQ','GOPG','KRS','BGS','AUBR','GAYA','MBI','BMKI','BGP','CPR','NWD','LKR','JHD','GRL','BAKA','PRNA','DMH','DBG','JUC','SASN','PTA','PTK','LDH','ASR','MSZ','HSX','KXH','MOGA','SAG','RPAR','FDK','FGSB','BNN','MKS','GSP','FZR','AST','GGN','FDB','PWL','SNP','CDG','UMB','PNP','KUN','SSA','ROK','HSR','YJUD','BNW','KKDE','KLE','JHJ','CKD','KUR','JJKR','BHC','BLS','BEH','KNPR','JNRD','PURI','KRPU','DNKL','CTC','RNC','BKSC','DTO','HZD','GHQ','BANO','DHN','DGHR','KQR','JMT','GRD','DDN','KGM','HW','HLDD','KTW','CDG','UHL','MDPB','HAR','KRBA','R','RJN','DURG','BSP','JTTN','KYQ','GLPT','DBB','NLV','CPK','SCL','LMP','GLGT','PDY','MAHE','KRMI','CNO']
        all_stations =['BBS','BPL','BSB','BZA','CNB','GZB','HWH','JP','KUR','KYN','AADR','AAL','AAM','AAR','AAS','AAY','AB','ABD','ABFC','ABI','ABKA','ABKP','ABLE','ABP','ABR','ABS','ABSA','ABU','ACLE','ACND','ACOI','AD','ADB','ADF','ADH','ADI','ADQ','ADR','ADRA','ADT','ADTL','ADTP','ADVI','AF','AFK','AFR','AGC','AGI','AGMN','AGN','AGR','AGTL','AGY','AH','AHA','AHH','AHN','AHQ','AI','AIG','AII','AIT','AJE','AJI','AJJ','AJL','AJNI','AJP','AJU','AK','AKD','AKE','AKJ','AKN','AKOR','AKP','AKT','AKV','AKVD','AL','ALB','ALD','ALER','ALJN','ALLP','ALM','ALMR','ALU','ALY','AMB','AME','AMG','AMH','AMI','AML','AMLA','AMLI','AMP','AMPA','AMRO','AMSA','AN','ANA','ANAH','ANAS','ANB','ANDI','ANDN','ANF','ANG','ANGL','ANH','ANK','ANKL','ANND','ANPR','ANR','ANSB','ANTU','ANV','ANVR','ANVT','ANY','AO','AONI','AP','APD','APDJ','API','APK','APN','APR','APT','AQG','ARA','ARAG','ARD','ARGD','ARJ','ARK','ARMU','ARQ','ARV','ARW','ASAF','ASD','ASH','ASK','ASKN','ASN','ASR','AST','ASTG','ATE','ATH','ATL','ATMO','ATNR','ATP','ATRU','ATS','ATT','ATU','AUB','AUBR','AUNG','AVD','AVN','AVRD','AVS','AWB','AWR','AWY','AY','AYRN','AYV','AYVN','AZ','AZR','BAB','BAF','BAGL','BAH','BAI','BAKA','BAL','BALU','BAM','BAMR','BAND','BANE','BANI','BANO','BAO','BAP','BAPR','BAQ','BARH','BARL','BAT','BATL','BAU','BAW','BAY','BAZ','BBA','BBGN','BBK','BBM','BBMN','BBN','BBTR','BBU','BC','BCA','BCH','BCHL','BCN','BCOB','BCRD','BCU','BCY','BD','BDBA','BDBP','BDC','BDCR','BDDR','BDGU','BDH','BDHY','BDJ','BDL','BDLN','BDM','BDMJ','BDN','BDRL','BDTS','BDU','BDVL','BDVT','BDW','BDWA','BDWD','BDWL','BDWS','BDY','BDYK','BDYR','BE','BEA','BEAS','BEB','BEG','BEH','BEHR','BEHS','BELA','BELD','BEM','BER','BET','BEY','BFD','BFJ','BFM','BFR','BG','BGAE','BGBR','BGH','BGHI','BGK','BGKT','BGM','BGND','BGNP','BGNR','BGP','BGPL','BGQ','BGRA','BGS','BGSF','BGTA','BGU','BGUA','BGVN','BGY','BGZ','BH','BHB','BHBK','BHC','BHD','BHET','BHI','BHKD','BHKH','BHL','BHLA','BHLE','BHLK','BHLP','BHME','BHP','BHRL','BHS','BHT','BHTA','BHTK','BHTN','BHTR','BHUJ','BHW','BHY','BIA','BID','BIDR','BIG','BIH','BIJR','BILD','BIM','BINA','BINR','BIO','BIRD','BIX','BIY','BJ','BJD','BJE','BJF','BJK','BJMD','BJNR','BJO','BJP','BJQ','BJR','BJRI','BJU','BJV','BJW','BKG','BKH','BKI','BKJ','BKL','BKN','BKNG','BKO','BKP','BKRD','BKRO','BKSC','BKSL','BL','BLA','BLAX','BLD','BLDA','BLDI','BLG','BLGR','BLGT','BLK','BLM','BLMK','BLMR','BLNR','BLO','BLP','BLPR','BLPU','BLQR','BLS','BLT','BLTR','BLU','BLW','BLX','BLZ','BMB','BMCK','BMD','BME','BMF','BMH','BMI','BMJ','BMKI','BMLL','BMO','BMR','BMSB','BMT','BMU','BN','BNA','BNC','BNCE','BNDA','BNDM','BNDP','BNE','BNG','BNGN','BNI','BNKI','BNLW','BNN','BNO','BNP','BNQ','BNR','BNSA','BNT','BNTL','BNU','BNV','BNVD','BNW','BNWC','BNXR','BNY','BNZ','BOBS','BOD','BOE','BOG','BOJ','BOKR','BOM','BON','BONA','BOR','BORA','BORD','BOTI','BOW','BOY','BP','BPA','BPB','BPC','BPF','BPH','BPHB','BPK','BPM','BPO','BPP','BPQ','BPR','BPRD','BPRH','BPRS','BPZ','BQA','BQG','BQI','BQP','BQQ','BQR','BQU','BRAG','BRC','BRD','BRE','BRG','BRGA','BRGT','BRGW','BRH','BRJN','BRKA','BRLF','BRMO','BRND','BRPL','BRPS','BRPT','BRQ','BRR','BRRG','BRS','BRU','BRUD','BRVR','BRW','BRWD','BRY','BRYA','BRZ','BSAE','BSC','BSCP','BSDP','BSE','BSGN','BSI','BSJ','BSKH','BSKR','BSL','BSM','BSP','BSPN','BSPR','BSPX','BSQP','BSR','BSRL','BSRX','BSSL','BST','BSTP','BSX','BSY','BSYA','BSZ','BTA','BTBR','BTD','BTE','BTG','BTH','BTI','BTIC','BTJ','BTJL','BTK','BTKP','BTO','BTP','BTPD','BTQ','BTRA','BTS','BTT','BTTR','BTU','BTV','BTW','BTX','BTY','BU','BUA','BUDI','BUDM','BUG','BUH','BUI','BUP','BUPH','BURN','BUT','BUTA','BUW','BUX','BV','BVC','BVH','BVI','BVL','BVN','BVNR','BVP','BVQ','BVRM','BVRT','BVU','BWH','BWI','BWIP','BWK','BWL','BWM','BWN','BWR','BWSN','BWT','BXC','BXHT','BXJ','BXN','BXP','BXR','BXY','BYD','BYL','BYN','BYNR','BYPL','BYT','BYZA','BZG','BZLE','BZM','BZN','BZO','BZR','BZU','BZY','CAA','CAER','CAF','CAG','CAI','CAN','CAP','CAPE','CAR','CBE','CBF','CBH','CBJ','CBK','CBM','CBN','CBSA','CBU','CC','CCH','CCK','CCT','CD','CDA','CDG','CDGR','CDM','CDMR','CDSL','CE','CGI','CGL','CGN','CGR','CGS','CGY','CH','CHA','CHB','CHD','CHDX','CHE','CHH','CHI','CHJ','CHKE','CHL','CHMG','CHNN','CHNR','CHOK','CHP','CHPT','CHR','CHRM','CHSM','CHTL','CHV','CHZ','CI','CIL','CIV','CJ','CJM','CJN','CJS','CJW','CKB','CKBK','CKD','CKDL','CKHS','CKI','CKNI','CKP','CKR','CKS','CKTD','CKU','CLD','CLDR','CLDY','CLF','CLG','CLJ','CLKA','CLR','CLT','CLU','CLX','CM','CMA','CMJ','CMNR','CMU','CMW','CMX','CNA','CNC','CND','CNDB','CNDM','CNGR','CNI','CNK','CNO','CNPA','CNPR','CNS','COA','COE','COM','COR','CPA','CPDR','CPH','CPJ','CPK','CPN','CPP','CPR','CPS','CPT','CPU','CQA','CRJ','CRKR','CRLM','CROA','CRP','CRR','CRWA','CRX','CRY','CSA','CSB','CSMT','CSN','CSTM','CSZ','CT','CTA','CTC','CTKT','CTND','CTO','CTR','CTRE','CTYL','CUK','CUPJ','CUR','CUX','CVP','CVR','CW','CWA','CWDA','CYN','DAA','DAB','DABN','DADN','DAJ','DAKE','DARA','DAS','DAVM','DBA','DBB','DBD','DBEC','DBG','DBL','DBLA','DBR','DBRG','DBRT','DBU','DBY','DD','DDA','DDCE','DDDM','DDE','DDL','DDN','DDP','DDR','DDU','DEB','DEC','DEE','DEEG','DEG','DEHR','DEOR','DEOS','DER','DES','DEV','DG','DGA','DGG','DGHA','DGHR','DGI','DGLE','DGO','DGR','DGU','DHA','DHD','DHE','DHG','DHI','DHN','DHND','DHNE','DHO','DHPR','DHR','DHRR','DHT','DHW','DIA','DIB','DIG','DIL','DING','DINR','DISA','DJG','DJHR','DJI','DJX','DKBJ','DKD','DKGN','DKGS','DKJ','DKJR','DKN','DKNT','DKO','DKT','DKZ','DL','DLB','DLD','DLGN','DLI','DLJ','DLK','DLN','DLO','DLPC','DLPH','DLQ','DLR','DLW','DMBR','DMC','DMG','DMGN','DMH','DMK','DMLE','DMM','DMN','DMNJ','DMO','DMR','DMRT','DMRX','DMT','DMV','DMW','DNA','DND','DNEA','DNK','DNKL','DNM','DNN','DNR','DNRE','DNT','DNV','DNWH','DO','DOA','DOB','DOD','DOE','DOL','DOR','DOS','DOTL','DOZ','DPA','DPJ','DPL','DPR','DPS','DPU','DPUR','DPZ','DQG','DQN','DR','DRD','DRH','DRI','DRL','DRLA','DRO','DRQ','DRSN','DRTP','DRU','DSA','DSB','DSJ','DSO','DSPN','DSR','DSS','DTAE','DTL','DTO','DTRD','DUA','DUB','DUBH','DUD','DUE','DUI','DUJ','DUMK','DUR','DURE','DURG','DUSI','DVD','DVG','DVL','DVM','DWDI','DWG','DWK','DWLE','DWO','DWP','DWR','DWX','DWZ','DXD','DXG','DXN','DYD','DZA','DZB','DZKT','ED','EDN','EE','EKC','EKI','EKM','EKMA','EKN','EKR','ELM','ENB','ERL','ERN','ERS','ET','ETM','ETP','ETUE','ETW','FA','FAN','FAP','FBD','FBG','FD','FDB','FDK','FDN','FGR','FGSB','FK','FKA','FKG','FKM','FL','FLK','FM','FN','FPS','FSP','FTD','FTG','FTP','FTS','FUT','FYZ','FZD','FZP','FZR','G','GA','GAD','GADH','GADJ','GAGA','GAJ','GAJB','GALE','GAM','GANG','GANL','GAP','GAR','GAUR','GAYA','GB','GBA','GBD','GBP','GBX','GCH','GCT','GD','GDA','GDB','GDG','GDL','GDO','GDP','GDR','GDV','GDX','GDYA','GEA','GED','GGA','GGC','GGJ','GGN','GGR','GGT','GGVT','GH','GHAI','GHD','GHGL','GHH','GHJ','GHNA','GHPU','GHQ','GHR','GHS','GHX','GHY','GID','GII','GIMB','GIN','GIO','GJD','GJH','GJL','GJN','GJS','GJUT','GKC','GKH','GKJ','GKK','GKP','GLA','GLG','GLGT','GLH','GLP','GLPT','GMAN','GMD','GMDA','GMDN','GMH','GMIA','GMO','GMR','GMS','GMTO','GNA','GNC','GND','GNG','GNGD','GNH','GNJ','GNK','GNP','GNPR','GNT','GNU','GNVR','GNW','GOA','GOC','GOGH','GOH','GOK','GOL','GOM','GOP','GOPG','GOTN','GOY','GP','GPAE','GPB','GPD','GPH','GPI','GPR','GPZ','GQL','GQN','GRA','GRBL','GRCP','GRD','GRH','GRKN','GRL','GRMA','GRMP','GRMR','GRO','GRRU','GRX','GRY','GSP','GSPR','GT','GTJT','GTK','GTL','GTM','GTNR','GTRA','GTS','GTST','GTT','GUB','GUD','GUG','GUH','GUNA','GUP','GUR','GUV','GVB','GVD','GVG','GVI','GVL','GVMR','GVN','GVR','GW','GWA','GWD','GWL','GWV','GY','GYM','GYN','GZH','GZM','GZN','GZO','HA','HAD','HAN','HAPA','HAR','HAS','HBD','HBJ','HBLN','HCNR','HCP','HCR','HD','HDA','HDB','HDE','HDGR','HDK','HDL','HDN','HDU','HDW','HEM','HG','HGH','HGL','HGT','HIJ','HIL','HIND','HIP','HIR','HISE','HJI','HJL','HJP','HKG','HLAR','HLDD','HLDR','HLKT','HLN','HLZ','HMG','HMH','HML','HMO','HMY','HN','HNA','HNK','HNL','HNS','HOJ','HP','HPLE','HPO','HPP','HPT','HPU','HRB','HRE','HRG','HRI','HRN','HRNR','HRPG','HRR','HRS','HRSN','HRT','HRV','HRW','HSA','HSD','HSDA','HSI','HSK','HSP','HSR','HSRA','HSX','HTC','HTE','HTK','HTZ','HTZU','HUP','HVD','HVR','HW','HWT','HX','HYB','HYT','HZBN','HZD','HZR','IAA','ICL','IDG','IDH','IDR','IGP','IGU','IJK','IKK','IKR','IMGE','INDB','IPL','IPM','IPR','IRA','ISA','ISH','ISM','ITA','ITR','IZN','J','JAA','JAB','JAC','JACN','JAIS','JAJ','JAL','JAM','JAMA','JAN','JAO','JAT','JBD','JBGD','JBN','JBP','JBX','JCL','JDB','JDH','JER','JES','JEUR','JGA','JGD','JGJ','JGJN','JGM','JGN','JGR','JHD','JHJ','JHL','JHN','JHS','JHW','JID','JIND','JIT','JJG','JJK','JJKR','JJN','JJR','JKA','JKB','JKE','JKN','JKNI','JKPR','JL','JLD','JLL','JLN','JLR','JLS','JLW','JLWC','JM','JMD','JMDG','JMK','JMKT','JMP','JMPT','JMQ','JMT','JMU','JMV','JNA','JND','JNH','JNKR','JNL','JNO','JNR','JNRD','JNU','JOA','JOB','JOBA','JOC','JOL','JOM','JOP','JOQ','JOR','JPD','JPE','JPG','JPH','JPL','JPZ','JRA','JRC','JRG','JRK','JRLE','JRLI','JRMG','JRPD','JRR','JRU','JSB','JSG','JSGR','JSM','JSME','JSP','JSR','JSV','JTB','JTI','JTJ','JTRD','JTTN','JTW','JU','JUC','JUCT','JUD','JUDW','JUJA','JVN','JWB','JWL','JWO','JWP','JYG','JYP','KAD','KAH','KAI','KAJ','KAJG','KAL','KAMG','KAN','KAP','KAPG','KAR','KARR','KART','KASR','KAT','KATI','KATL','KAW','KAWR','KAWT','KAYR','KBE','KBI','KBJ','KBL','KBM','KBPR','KBQ','KBRV','KBY','KCA','KCC','KCD','KCF','KCG','KCI','KCJ','KCKI','KCR','KCT','KCV','KCVL','KDF','KDG','KDHA','KDJR','KDKN','KDM','KDMR','KDNL','KDP','KDPR','KDRP','KDU','KEA','KED','KEG','KEH','KEI','KEK','KEM','KEMA','KEN','KEPR','KER','KESR','KEX','KFA','KGA','KGB','KGG','KGI','KGL','KGLE','KGM','KGP','KGQ','KGS','KGX','KH','KHBJ','KHDB','KHED','KHGP','KHH','KHM','KHMA','KHNM','KHRJ','KHRK','KHS','KHT','KHTU','KHU','KI','KIGL','KIK','KIM','KIN','KIP','KIR','KIS','KIT','KIUL','KJ','KJA','KJG','KJH','KJI','KJM','KJN','KJT','KJU','KJY','KJZ','KK','KKA','KKAH','KKB','KKDE','KKDI','KKGM','KKHT','KKI','KKJ','KKLR','KKLU','KKM','KKN','KKNA','KKP','KKPM','KKTA','KKU','KKW','KKY','KKZ','KL','KLAR','KLB','KLBG','KLD','KLE','KLG','KLGD','KLJ','KLK','KLKA','KLL','KLNK','KLP','KLPG','KLPM','KLQ','KLRE','KLRS','KLT','KLTR','KLU','KLYT','KMAE','KMBL','KMC','KMD','KMDR','KMGE','KMJ','KML','KMME','KMNC','KMNR','KMQ','KMS','KMT','KMU','KMX','KMZ','KN','KND','KNE','KNF','KNHP','KNJ','KNL','KNLS','KNN','KNNK','KNP','KNPR','KNPS','KNRT','KNS','KNT','KNVT','KNW','KO','KOAA','KOHR','KOI','KOJ','KOLI','KOLR','KON','KONY','KOO','KOP','KOTA','KOU','KOV','KP','KPD','KPG','KPGM','KPI','KPKI','KPL','KPN','KPNA','KPO','KPP','KPQ','KPRD','KPRR','KPTN','KPV','KPY','KPZ','KQK','KQL','KQN','KQR','KQT','KQU','KQW','KRA','KRAR','KRBA','KRBP','KRD','KRDL','KRE','KRG','KRH','KRIH','KRJ','KRLA','KRLI','KRLR','KRMI','KRMR','KRND','KRNR','KRNT','KRPP','KRPU','KRR','KRS','KRSA','KRSL','KRY','KS','KSB','KSC','KSD','KSF','KSG','KSH','KSJ','KSM','KSN','KSNG','KSP','KSRA','KSTA','KSV','KSW','KSWR','KSX','KT','KTCH','KTE','KTES','KTGA','KTH','KTHD','KTHU','KTJ','KTKL','KTM','KTMA','KTO','KTPR','KTQ','KTRH','KTRK','KTRR','KTSH','KTU','KTV','KTW','KTX','KTYM','KUA','KUD','KUDA','KUDL','KUE','KUF','KUGT','KUH','KUK','KUKA','KUMB','KUN','KUPR','KURJ','KURT','KUTI','KUU','KUV','KUX','KVG','KVK','KVM','KVR','KVU','KVZ','KWAE','KWE','KWH','KWM','KWO','KWP','KWR','KWV','KXB','KXG','KXH','KXL','KXN','KY','KYE','KYF','KYJ','KYM','KYOP','KYQ','KYT','KYX','KZA','KZB','KZE','KZJ','KZK','KZT','KZTW','KZY','LAD','LAR','LAU','LAV','LBA','LC','LCAE','LD','LDA','LDH','LDK','LEDO','LGH','LGL','LGO','LHA','LHLL','LHU','LIR','LJN','LJR','LKA','LKE','LKG','LKMR','LKN','LKO','LKR','LKS','LKU','LKW','LKZ','LLGM','LLI','LLJ','LLR','LM','LMG','LMK','LMN','LMNR','LMO','LMP','LMT','LNH','LNK','LNL','LNN','LNR','LNT','LOA','LPI','LPJ','LPJL','LRD','LRJ','LS','LSI','LSR','LSX','LTD','LTHR','LTR','LTRR','LTT','LUNI','LUR','LUSA','LWR','LWS','LXA','MA','MAAR','MABA','MABD','MAD','MAG','MAGH','MAHE','MAI','MAJN','MAKM','MAKR','MALB','MALM','MAM','MAN','MANG','MAO','MAP','MAQ','MAR','MAS','MAU','MAUR','MAY','MB','MBA','MBB','MBF','MBG','MBGA','MBI','MBM','MBNL','MBNR','MBS','MBY','MCA','MCI','MCN','MCQ','MCS','MCSC','MCU','MDB','MDDP','MDE','MDF','MDGR','MDJ','MDJN','MDKD','MDL','MDLE','MDN','MDNR','MDP','MDPB','MDR','MDS','MDT','MDU','MDVK','MDVL','MDW','MED','MEH','MEJ','MEM','MEP','MEQ','MET','MEW','MEX','MFJ','MFKA','MFL','MFP','MFQ','MG','MGAE','MGB','MGD','MGF','MGG','MGLE','MGLP','MGME','MGN','MGR','MHAD','MHBA','MHC','MHD','MHH','MHI','MHJ','MHO','MHPE','MHPR','MHQ','MHRG','MHT','MHV','MID','MIH','MIL','MIM','MINA','MINJ','MIPM','MJ','MJA','MJBT','MJF','MJG','MJKN','MJL','MJN','MJRI','MJS','MJZ','MK','MKA','MKB','MKC','MKDD','MKDI','MKH','MKN','MKO','MKP','MKPR','MKR','MKRH','MKRN','MKS','MKSR','MKU','MKX','ML','MLAR','MLB','MLD','MLDT','MLG','MLGH','MLHA','MLJ','MLMR','MLNH','MLO','MLP','MLPR','MLTR','MLV','MLX','MLY','MLZ','MMA','MMB','MMCT','MMD','MME','MMH','MMK','MMKB','MML','MMM','MMR','MMS','MMVR','MMY','MMZ','MNAE','MND','MNDR','MNE','MNF','MNGD','MNI','MNJ','MNM','MNO','MNP','MNQ','MNS','MNSR','MNTT','MNV','MNVL','MO','MOF','MOG','MOGA','MOI','MOJ','MOL','MOM','MOMU','MON','MONR','MOO','MOP','MOR','MOT','MOTC','MOTH','MOU','MOZ','MPA','MPH','MPI','MPL','MPLM','MPLR','MPU','MPY','MQ','MQO','MQR','MQS','MQU','MQX','MRA','MRB','MRBL','MRDG','MRDL','MRDW','MRE','MRG','MRGA','MRHA','MRHT','MRIJ','MRJ','MRK','MRL','MRN','MRND','MRPR','MRR','MRSH','MRT','MRTL','MRX','MS','MSDG','MSDH','MSDN','MSH','MSK','MSMD','MSR','MST','MSV','MSW','MSZ','MTC','MTD','MTH','MTHP','MTJ','MTM','MTP','MTPC','MTPI','MTPR','MTR','MTU','MTY','MUD','MUE','MUGA','MUGR','MULK','MUR','MURD','MURI','MUT','MUV','MUW','MV','MVI','MVJ','MVLK','MVN','MVO','MW','MWAD','MWJ','MWK','MWM','MWRN','MWT','MWX','MXH','MXK','MXN','MXR','MXT','MYA','MYG','MYK','MYR','MYS','MYY','MZC','MZH','MZL','MZM','MZP','MZR','MZS','NAB','NAC','NAD','NAK','NAL','NAM','NAN','NANA','NANR','NASP','NAT','NAVI','NAW','NAZJ','NB','NBA','NBD','NBG','NBH','NBI','NBL','NBQ','NBR','NCB','NCH','NCJ','NCR','ND','NDAE','NDB','NDD','NDJ','NDKD','NDKR','NDL','NDLS','NDN','NDO','NDT','NDU','NDW','NED','NEO','NEW','NFK','NG','NGA','NGAN','NGB','NGE','NGG','NGI','NGN','NGNT','NGO','NGP','NGR','NGT','NGY','NH','NHH','NHK','NHLG','NHLN','NHN','NHR','NHT','NHY','NIA','NIL','NILE','NIQ','NIRA','NIU','NJA','NJN','NJP','NJT','NK','NKB','NKD','NKE','NKJ','NKK','NKM','NKMG','NKP','NKRA','NKW','NLD','NLDA','NLDM','NLE','NLI','NLKR','NLP','NLR','NLV','NMDA','NMG','NMGA','NMGT','NMGY','NMH','NMJ','NMK','NMKL','NMM','NMT','NMX','NMZ','NN','NNA','NNGE','NNKR','NNL','NNN','NNO','NNR','NNW','NOI','NOK','NOLI','NOMD','NOQ','NPD','NPK','NPNR','NPRD','NPS','NQR','NR','NRA','NRDP','NRE','NRG','NRGR','NRI','NRKR','NRL','NRLR','NRM','NRO','NRP','NRPA','NRR','NRS','NRT','NRW','NRZB','NS','NSD','NSL','NSU','NSX','NTSK','NTV','NTW','NU','NUA','NUD','NUH','NUQ','NUR','NVG','NVS','NW','NWB','NWD','NWH','NWP','NWR','NWU','NXN','NYG','NYGT','NYH','NYK','NYN','NYO','NYP','NYY','NZB','NZD','NZM','NZT','OBR','OBVP','OCR','ODB','ODC','ODG','ODM','OEA','OGL','OKA','OKHA','OML','OMLF','ON','OPL','ORAI','ORGA','ORR','OSN','OTP','OYR','PAD','PAI','PAIL','PAK','PALM','PAM','PAN','PANP','PAO','PAP','PAR','PARH','PASA','PAU','PAV','PAW','PAY','PAZ','PB','PBE','PBH','PBKS','PBL','PBM','PBN','PBP','PBR','PBW','PC','PCH','PCM','PCN','PCV','PCZ','PDD','PDF','PDH','PDKN','PDKT','PDL','PDPL','PDRD','PDT','PDU','PDW','PDWA','PDY','PEH','PEM','PEP','PER','PERN','PES','PFL','PFM','PFR','PFT','PGA','PGI','PGK','PGR','PGRL','PGT','PGTN','PGW','PHA','PHD','PHK','PHLG','PHN','PHR','PIA','PIH','PIL','PIP','PIRO','PIS','PIT','PJ','PKD','PKF','PKO','PKPU','PKQ','PKR','PKU','PKW','PLCJ','PLG','PLH','PLI','PLJ','PLJE','PLM','PLMD','PLNI','PLO','PLP','PLS','PLSN','PLY','PM','PMK','PMKT','PML','PMN','PMP','PMR','PMT','PMU','PMY','PNBE','PNC','PND','PNDM','PNE','PNF','PNHR','PNKD','PNME','PNP','PNQ','PNSA','PNU','PNVL','PNW','PNYA','POA','POE','POK','POR','POT','POU','POY','POZ','PPA','PPC','PPD','PPI','PPN','PPO','PPR','PPT','PPTA','PPU','PPW','PPZ','PQL','PQN','PRB','PRDL','PRDP','PRDT','PRF','PRG','PRGR','PRH','PRI','PRL','PRLI','PRNA','PRNC','PRND','PRNR','PRP','PRR','PRT','PRWD','PRY','PS','PSA','PSAE','PSB','PSD','PSE','PSLI','PSR','PTA','PTB','PTH','PTHD','PTI','PTJ','PTK','PTKC','PTKD','PTKP','PTN','PTNR','PTPL','PTRD','PTRE','PTRU','PTT','PTU','PU','PUK','PUL','PUN','PUNE','PUO','PURI','PUS','PUSA','PUT','PUU','PUX','PVD','PVP','PVPT','PVR','PVRD','PVU','PWL','PWS','PYD','PYG','PYOL','QLD','QLM','QLN','QRP','QSR','R','RAA','RAG','RAIR','RAJP','RAL','RANI','RASP','RAY','RBA','RBD','RBG','RBK','RBL','RBS','RBZ','RC','RCTC','RDDE','RDHP','RDL','RDM','RDN','RDP','RDRA','RDUM','RE','RECH','REI','REJ','REN','REWA','RFJ','RG','RGD','RGDA','RGH','RGJ','RGL','RGO','RGP','RGPM','RGS','RGU','RHA','RHE','RHG','RHMA','RHN','RIG','RJA','RJG','RJK','RJN','RJO','RJP','RJPB','RJPM','RJR','RJT','RJY','RK','RKB','RKD','RKL','RKM','RKSH','RKSN','RKZ','RLA','RLO','RM','RMA','RMB','RMC','RMD','RMF','RMGM','RMJK','RMM','RMN','RMNP','RMP','RMPB','RMPR','RMR','RMRB','RMT','RMU','RN','RNC','RNE','RNG','RNGG','RNH','RNO','RNPR','RNQ','RNR','RNV','RNW','RNY','ROA','ROHA','ROI','ROK','ROP','ROU','ROZA','RPAN','RPAR','RPD','RPH','RPJ','RPMN','RPO','RPR','RPRD','RPUR','RPZ','RQJ','RRB','RRME','RRS','RSH','RSI','RSJ','RSKA','RSNR','RSR','RT','RTA','RTGH','RTI','RTM','RTMN','RTP','RU','RUL','RUM','RUPC','RUR','RURA','RUSD','RUT','RV','RVK','RVKH','RWH','RWJ','RWL','RWO','RWTB','RXL','RYP','RYS','S','SA','SAA','SAC','SADP','SAG','SAGR','SAH','SAHI','SAI','SALE','SAN','SANR','SAO','SAP','SAS','SASN','SAT','SAU','SAV','SAW','SBB','SBBJ','SBC','SBD','SBDR','SBE','SBG','SBGA','SBHR','SBIB','SBLT','SBM','SBO','SBP','SBPD','SBPY','SBR','SBRA','SBT','SBV','SBZ','SC','SCC','SCE','SCH','SCI','SCKR','SCL','SCM','SCT','SD','SDAH','SDB','SDBH','SDE','SDF','SDGH','SDI','SDL','SDLK','SDLP','SDMD','SDN','SDNR','SDS','SDT','SEB','SED','SEE','SEG','SEGM','SEH','SELU','SEM','SEO','SET','SEU','SFA','SFC','SFG','SFH','SFM','SFMU','SFR','SFW','SFY','SGAM','SGBJ','SGD','SGDM','SGDP','SGE','SGF','SGG','SGJ','SGL','SGLA','SGNR','SGO','SGP','SGR','SGRA','SGRE','SGRL','SGRM','SGRR','SGUJ','SGZ','SHC','SHDM','SHDR','SHE','SHF','SHG','SHK','SHM','SHNG','SHNR','SHNX','SHR','SHRN','SHSK','SHTT','SHU','SHV','SI','SID','SIHO','SIKR','SIL','SILO','SIM','SINI','SIOB','SIP','SIPR','SIQ','SIR','SIRD','SIW','SJN','SJNP','SJP','SJQ','SJT','SKA','SKB','SKF','SKGH','SKI','SKIP','SKJ','SKLR','SKM','SKN','SKND','SKP','SKPA','SKPI','SKPT','SKR','SKS','SKT','SKTN','SKZR','SL','SLB','SLD','SLF','SLGR','SLH','SLI','SLJ','SLKR','SLKX','SLN','SLNA','SLO','SLT','SLW','SLY','SM','SMAE','SMBJ','SMBL','SMBX','SMCP','SMD','SME','SMET','SMI','SMK','SMLA','SMND','SMNH','SMO','SMP','SMPA','SMPR','SMQL','SMR','SMRL','SMRR','SMT','SMZ','SNC','SNDD','SNF','SNGN','SNGP','SNI','SNK','SNKL','SNL','SNLR','SNM','SNN','SNP','SNQ','SNRR','SNSI','SNT','SNTD','SNV','SNX','SOA','SOAE','SOD','SOG','SOJN','SONI','SOP','SOR','SORO','SOS','SOT','SPC','SPDR','SPE','SPJ','SPK','SPLE','SPN','SPP','SPQ','SPRD','SPT','SPTR','SPX','SPZ','SQL','SQN','SQR','SRAS','SRBA','SRC','SRE','SRF','SRGH','SRGM','SRGT','SRI','SRID','SRJ','SRKI','SRNK','SRNR','SRNT','SRO','SRP','SRPJ','SRPM','SRR','SRT','SRTL','SRTN','SRU','SRUR','SRW','SRY','SSA','SSB','SSD','SSDT','SSIA','SSL','SSM','SSPN','SSR','ST','STA','STBJ','STD','STJT','STKT','STKW','STL','STLR','STN','STNL','STP','STPD','STR','STW','SUA','SUD','SUJH','SUJR','SUNR','SUR','SURI','SURL','SV','SVA','SVDK','SVGA','SVHE','SVJR','SVKD','SVKS','SVM','SVPI','SVPR','SVRP','SVV','SVX','SWA','SWC','SWE','SWF','SWM','SWPR','SWR','SWRT','SWV','SXP','SXT','SY','SYA','SYC','SYJ','SYL','SYN','SYWN','SZ','SZM','SZR','TA','TAE','TAN','TAPA','TATA','TAZ','TBAE','TBH','TBM','TBN','TBR','TBT','TCH','TCL','TCN','TCR','TDD','TDL','TDLE','TDN','TDO','TDP','TDPR','TDU','TEA','TEL','TELO','TELY','TEN','TET','TETA','TFGN','TGA','TGN','TGP','TGQ','TGRL','TGU','TH','THA','THAN','THB','THBN','THDR','THE','THL','THMR','THUR','THV','THVM','TIA','TIBI','TIG','TIHU','TIR','TIS','TIU','TIW','TJ','TK','TKBG','TKC','TKD','TKE','TKG','TKH','TKJ','TKMG','TKN','TKQ','TKR','TKRI','TL','TLC','TLD','TLGP','TLH','TLHD','TLHR','TLJ','TLKH','TLM','TLR','TLU','TLV','TLWA','TLY','TME','TMKA','TML','TMQ','TMR','TMV','TMX','TMZ','TN','TNA','TNGL','TNKU','TNL','TNM','TNR','TOI','TORI','TP','TPF','TPH','TPJ','TPK','TPT','TPTN','TPTY','TPU','TPY','TPZ','TQA','TQM','TR','TRAN','TRB','TRK','TRL','TRO','TRR','TRS','TRT','TRTR','TRVL','TRWT','TSA','TSD','TSF','TSI','TSK','TSR','TTB','TTL','TTR','TU','TUA','TUG','TUL','TUN','TUNI','TUP','TUV','TUVR','TVC','TVG','TVP','TVR','TWB','TWG','TZR','UA','UAA','UB','UBC','UBL','UBR','UCA','UCR','UD','UDGR','UDL','UDM','UDN','UDR','UDT','UDZ','UGR','UHL','UHP','UHR','UJ','UJA','UJH','UJN','UJP','UKA','UKL','UKR','ULB','ULD','ULG','ULL','ULT','UMB','UMD','UMED','UMR','UMRI','UR','URD','UREN','URGA','URI','URL','URPR','USL','UTA','UTL','UTR','UVD','VAA','VAK','VAPI','VAPM','VARD','VBL','VBW','VDA','VDD','VDE','VDL','VDS','VEER','VG','VGE','VGN','VHGN','VI','VID','VJA','VJP','VJPJ','VKA','VKB','VKI','VKN','VKR','VLD','VLI','VLNK','VLR','VLT','VLY','VM','VMA','VMD','VMU','VN','VNA','VNB','VNE','VNUP','VPDA','VPO','VPT','VPZ','VR','VRB','VRG','VRH','VRI','VRL','VRR','VRX','VS','VSG','VSKP','VST','VSU','VTJ','VTM','VV','VVM','VYA','VYK','VYN','VZM','VZR','WAB','WADI','WANI','WC','WDM','WDR','WENA','WFD','WHM','WIRR','WJR','WKI','WKR','WL','WLGN','WOC','WPR','WR','WRR','WRS','WSA','WSJ','WTJ','WTR','WZJ','XBKJ','Y','YA','YDM','YFP','YG','YJUD','YL','YLG','YLM','YNK','YP','YPR','YY','ZB','ZBD','ZN','ZNA','ZRDE']
        l=[]
        
        
        for z in h:
            t = z.strip("\n")
            l.append(t)
        
        dict={}
        
        for x in l:
            dict[x]= 1
        
        for x in f:
            t = x.split(" ")
            if math.floor(float(t[2])) < int(dist):
                n = (int(dist) - math.floor(float(t[2])))/int(dist)
                if t[1] not in dict:
                    dict[t[1]] = n
                elif dict[t[1]] < n:
                    dict[t[1]] = n
                
                    
        f2 = open('2_Distances_from_the_Hotspots.txt','r')   
        
        
        for x in f2:
            t = x.split(" ")
            if math.floor(float(t[2])) < int(dist):
                n2 = (int(dist) - math.floor(float(t[2])))/int(dist)
                if t[1] not in dict:
                    dict[t[1]] = n2
                elif dict[t[1]] < n2:
                    dict[t[1]] = n2
        
        g = open('F_Numbering.txt','w')
        
        
        for w in all_stations:
            if w not in dict:
                dict[w] = 0
            
        for y in dict.keys():
            g.write(str(y)+" "+str(dict[y])+"\n")   

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def working_list():
        num = tnum
        f = open('F_Numbering.txt','r')
        g = open('Working.txt','w')
        
        for x in f:
            t = x.split(" ")
            n = float(t[1])
            #print(n)
            
            if n < float(num):
                g.write(t[0]+"\n")

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

def making_new_routes():
        f = open('Trains_routes_original_with_Distances.txt','r')
        g = open('new_routes_with_distances.txt','w')
        h = open('Working.txt','r')
        #working = ['CKP','BSP','NGP','KYN','B','D']
        #working = ['ABKP','BSPR','KTO','BRH','BJRI','KTMA','APR','BUH','BRS','UMR','KTES','KLPG','KJZ','SJQ','SPDR','NGE','DTL','NPRD','UKR','BRND','BATL','HRV','DRSN','MZH','JTI','PND','KNVT','BHBK','HEM','UMRI','RGP','GNP','CJM','ANB','OGL','TNR','VKI','KHT','DXG','BUA','KHS','RIG','GP','ROU','CKP','TATA','SPE','PDWA','JWB','MJ','HP','GOTN','LGH','BBMN','JAT','JLR','JND','KSD','MLHA','CVR','VRL','SRPJ','CKB','IDG','RTA','GUNA','ASKN','MNV','DMO','KMZ','DGR','AB','VN','SYWN','MNJ','BRE','SJT','KGA','FYZ','ANV','TUNI','NRP','YLM','AKP','DVD','SCM','KTV','VBL','PVP','PVPT','RGDA','SPRD','THV','MNGD','NRLR','RPRD','TIG','BUDM','BLGR','BRPL','BRGA','ATS','SBP','SBPD','NXN','BNDM','RKSN','SINI','ADTP','NRKR','PAR','PPI','BKH','GAR','KY','NU','BOE','NOQ','SRJ','DBR','MKP','JTW','STA','REWA','RGJ','RDP','SRU','BTT','MW','SMI','BUG','HIR','NKE','BRU','PANP','TTR','ASK','DRU','RRB','AJP','APDJ','KWM','LMG','HOJ','HSA','NMZ','AUB','KDPR','HCR','MLDT','NFK','PKR','SNT','AMP','LAV','JOQ','RVK','KCF','HAN','GGC','SGZ','NAD','SKF','LAR','CSN','MMR','PAU','AMG','GHR','STL','OYR','KAN','JLN','DUA','ODG','HD','CHA','JMV','MLV','BBN','DPS','KNPS','CBSA','NOMD','GTS','DJHR','MMVR','BSPX','JRLI','NYG','PRNR','GADH','KDJR','NANR','BSTP','STBJ','HCNR','CLDR','BGY','CAP','BAM','IPM','PSA','BMCK','LJR','DPUR','SPT','SEM','DD','KJT','KIT','VKN','DKD','MRK','CBM','GID','DMT','GY','HUP','GBD','RSKA','CLKA','GAM','KTGA','SKPI','BLMK','LLGM','RUL','TKRI','SGRM','KPRR','JDB','RBA','MMS','BONA','BAMR','RAIR','HKG','LSX','MOI','SGNR','SRGT','JVN','BSR','RNH','VMA','THUR','SVA','DKNT','GQL','KPTN','KPZ','LKE','MLZ','NNW','LTR','DHG','BCOB','GIMB','AI','AJE','BHUJ','AIG','HG','YG','AD','DUMK','SKIP','PRGR','TPH','BHW','GMAN','SURI','PAW','KPRD','RMPR','KEMA','RUT','BMSB','COE','PDF','AAR','KOHR','PAV','MYR','KTE','KMNC','NAC','RSNR','GJS','SRW','KESR','BLGT','GRMP','GZO','EKI','SM','BKRD','TKG','MKRH','RMPB','MLNH','BNDP','DOTL','ADF','OMLF','RJG','BLT','SMR','MHJ','MKRN','LDA','GW','GAJ','PHA','ANA','KYX','BNU','GEA','SAO','SYA','BQQ','REI','HDU','JLW','RPD','VYK','CHD','LOA','KKI','NRZB','GGT','BDWA','AAL','CLF','NIQ','VKR','HRB','SBRA','KOI','MDGR','PRDL','CHRM','SJP','AKD','JBX','KKB','BNE','SCKR','GVB','PIA','ORR','SHDR','PGA','MUGA','RWJ','DPZ','SURL','ISA','SRAS','GA','GVMR','NYK','THMR','JOM','KXG','UMED','RGPM','PQL','ARGD','CNPR','DNEA','JAN','TORI','RNQ','CPU','AGY','CUK','SBDR','TPU','NGN','OBR','SGRL','KRLR','KRSL','SKTN','BRG','MBA','BTX','HPP','GLH','KJ','NWR','KDHA','CHDX','JKE','UDR','UHR','BGHI','TZR','BWT','TCL','KCD','TLU','PDL','KLKA','TU','KOU','KDP','KWV','KPN','CVP','MEJ','MVN','TME','TN','RLO','KSM','BSM','GDP','MAR','CNI','KND','MJG','ANPR','LNN','WTR','KRG','BGVN','JEUR','MA','MO','AKOR','SADP','MTU','KGL','NRR','LSR','NSL','PMKT','JMD','RM','MWK','NGI','TAE','NRL','RMP','TAZ','MSR','SIW','RAJP','KKW','KUDL','VID','KT','BTJL','BYNR','KUDA','TR','ANK','BLA','SGRR','MNVL','RMJK','UHP','SVDK','BDYR','APD','CRX','DPU','DMV','NTSK','DBRG','MRHT','BOJ','DJG','NHK','NAM','DGLE','DBRT','SUJH','LAU','KHTU','TLC','DGHA','KATI','RMRB','DKGN','RPAN','NMM','DKJR','MJBT','RWTB','ULG','HRSN','BNSA','MGB','KRY','MCU','MPL','VLD','MOR','NAN','MSMD','BGBR','KRAR','NPD','HSK','KBJ','SFC','DJX','GOL','SWR','HAS','HLN','PNHR','PARH','KCR','KLRS','LWS','BDWS','RSJ','MINA','TRWT','DHR','MTPC','BLO','YL','KPG','JSV','BPRH','BDGU','VNE','GPZ','TBH','HMY','GMTO','NHLN','LKG','BRLF','DSR','LXA','SFR','SPK','BFD','TSK','MJN','DBY','MRG','LEDO','JSR','MIPM','PDT','KPL','ALM','GPI','SNM','NSX','GMDA','KNRT','JMPT','CNPA','HDB','ORGA','KLG','GPH','SSIA','TUL','HIJ','KTJ','TDLE','UKA','DUJ','BRGW','SGAM','MWJ','BEHR','VST','KHBJ','JPH','RHE','BHLA','GPAE','PSAE','SXP','CMX','JMQ','GZM','PPO','KXN','PFR','BRRG','CBK','KHRJ','RTMN','NLI','PTHD','MSV','PLCJ','RDRA','AQG','POK','MWT','BAF','SIRD','NKRA','SBM','SUD','POT','TBR','ADQ','KNJ','MMD','KUD','RBG','UGR','CNC','CKR','AMSA','KVK','DLGN','SGLA','PVR','MLB','CDSL','CRKR','MRBL','KRDL','BCHL','DWZ','KKLU','DMK','ARK','KURJ','BVU','HML','KTPR','NLP','GOM','BDLN','DMC','SPTR','SMCP','TQM','MZS','PS','GOK','HNA','MRDW','BKJ','CHPT','SMPA','BUDI','DWK','MTHP','OKHA','BDDR','NKJ','MFQ','JOBA','NWB','GAJB','SDNR','SVV','NZT','KZB','ANY','KZY','TCN','KDU','SVPR','RJPM','SNKL','KDNL','SCT','AVS','PBKS','TPY','TKE','BDVT','SMET','ANF','SRF','TLGP','SET','SME','KLPM','DJI','PCM','KKY','ASD','JUJA','GMH','TPF','RNV','MBNL','MON','JOR','MKSR','SOA','ATU','CHSM','MHV','RLA','SVKD','LMO','AGTL','ABSA','DMR','NKMG','BPB','NHLG','PTKD','MBG','MHQ','NAB','WSA','PDD','NASP','BTW','BIJR','CHB','MXR','KTX','DMGN','MBGA','TLJ','KLP','VJP','CJN','DZKT','HLZ','GNPR','BGND','DRQ','LAD','THE','MEW','SBHR','SKLR','MCQ','MBF','WOC','KWE','KHGP','MCSC','MWAD','PUSA','SLJ','PRWD','KUGT','ASTG','PTPL','GIO','PLSN','BOTI','MSDG','JTRD','SGRE','ETP','KKLR','RU','SKT','BRD','KKN','MLGH','BZR','JBGD','NCB','BELD','NKW','KOJ','AKVD','KXB','FBD','VVM','AJU','NDAE','BMB','MRE','RC','SDLP','AGR','JES','KAJ','BHY','CLU','CMU','SNQ','SSPN','KLU','RHA','POR','MGF','TNL','SLKX','MDT','ODM','KZA','RPH','RHG','AZR','SOAE','DLPH','BTY','PKD','SMAE','KLAR','OBVP','UA','GDX','JKB','SHTT','PFL','NNL','SNRR','KPP','YDM','FTP','SBR','KWAE','NHY','VRR','ROZA','KJG','BRPS','ABKA','KKA','GAGA','HISE','JMDG','NDL','BVRT','KSN','PNE','SRO','KMX','BVRM','HVR','SHF','UDL','BGAE','KAMG','CAG','DNV','MHBA','SBE','PIH','SIOB','LKS','MTM','BILD','CLR','TUN','SAHI','GIN','BGNP','TETA','RGO','SHV','BBA','SPLE','SRI','BGRA','CKBK','BDBA','MDVL','GBX','SNSI','PKF','LDK','NRA','SBG','JRPD','MRB','BHTA','BJNR','SRKI','JIT','FKA','PAN','KNE','SDGH','HGT','BMD','PUN','MRR','CTR','BWL','LKZ','MHPR','SHG','CHNN','MLG','BSGN','CKU','VTM','MOU','ANKL','GOH','PRB','KHMA','RGL','RMB','PKO','RJR','FL','NDKR','GVD','GBP','SEU','TPTY','SBPY','KCI','SEG','FAP','BNLW','PLH','HN','BAU','BUI','PEP','DXN','DABN','BHP','PUT','BDWL','NYP','PB','BGNR','FA','SBD','LKA','KTSH','TBN','DIG','NYGT','WR','DTRD','CKTD','NRI','KGG','PSR','VMD','DTAE','BTRA','SBGA','MTD','DBLA','DEOS','SGRA','MNS','MRDG','KSRA','AMB','ADVI','NUD','CKHS','ACOI','BXJ','DNT','VDD','KAP','MKN','KMAE','KH','MGD','KMJ','LPI','ZB','DUD','EE','NAK','DOR','PTU','HZBN','GLP','SMBX','SALE','KEM','GPB','MCA','AMLA','KQW','BNTL','GRBL','PRLI','GOGH','NYN','RNG','PRH','BPRD','SLGR','MGME','BYD','VJPJ','SWF','MKR','LIR','SMO','NPNR','BSRX','SONI','LRD','LWR','SFG','CAI','SDS','BQA','PMT','UDT','BORA','BJMD','COA','JAA','JRA','SBLT','DMLE','CKNI','SGF','MURD','MOG','JAMA','BRVR','KKDI','MDVK','RNW','BJF','VSU','MRPR','WTJ','KOLR','AHN','MJA','PLM','RAL','LTHR','KVM','BZO','DLO','MUGR','CRR','MURI','JAJ','PMP','SI','KEN','CPH','PRDP','SRNR','DLK','BTK','DIA','KOLI','MMKB','KJU','DMBR','YP','HPT','BPH','BNA','ALD','BMU','URPR','MZC','DLQ','HDGR','KLRE','LNL','SGP','RMC','MSK','KBPR','SMPR','CLX','CCT','DQN','RUSD','NOK','NKB','TMR','JHL','PYG','NHT','MOJ','GVL','RV','KDG','JBN','PGRL','VG','KEK','MAKR','MOMU','KBL','KAWT','DPL','DEB','SWC','ALY','HJI','SPX','OSN','MLPR','UBR','SPN','JDH','ADRA','KAYR','PAP','DXD','SKPA','AMLI','GGVT','RMR','RHMA','DADN','MINJ','TSD','GRMR','BDH','NHR','KUU','MJZ','NMH','DHT','BTI','FLK','DLD','UTA','SRTN','TMZ','KGS','KRBP','MAAR','BSRL','FKM','NWP','GKK','DLR','CROA','KSNG','DDCE','NIRA','SY','KFA','BOW','NW','BTIC','BKI','DBU','BNV','KUK','KIR','MHI','RG','MDF','BLTR','BPO','KATL','SAH','TBT','NBQ','THAN','NJN','RURA','JIND','LKMR','BZY','KUKA','MDR','TBAE','AN','BNGN','JOC','TFGN','BU','BRJN','VZR','HSI','MOO','BINA','PRG','KSP','MKPR','RANI','BARH','IDR','NIA','TLH','SNLR','HDA','PPR','PLP','RMM','CMNR','BER','BGU','ANR','MDKD','AONI','KIGL','PLNI','DHND','BSAE','SRGH','LGO','BRUD','PPZ','ABP','EKM','STW','NTV','RJP','AL','DZB','KUMB','DLJ','PPT','NRDP','MHRG','LS','JKA','GALE','KBY','POA','PSD','DBL','NAZJ','SPJ','PNW','BJQ','KRD','TH','RMN','JRLE','CGI','MZR','GBA','SGDP','RNE','TKR','KNLS','PIT','GAUR','MRN','BOBS','JMU','SYL','NG','KTRR','JM','HSDA','MNAE','KAPG','SJN','GNA','WC','DHNE','FPS','RAY','SNC','SYC','BEAS','NMT','MRSH','ABR','SRID','JER','FGR','BMH','PRDT','PIL','GTL','CC','TRAN','NJA','HLAR','SAN','SDT','JYG','CJS','BTKP','UCA','KQT','UJP','NZD','CHR','RTGH','MTR','MOTH','GMIA','GMD','KEG','RXL','AAS','PJ','VZM','MTY','HWT','PQN','BDC','NMK','QLM','MSW','ENB','BNG','HGH','DRD','LNT','RDL','DUE','PNYA','TOI','BV','TSF','BTTR','PHN','JOB','IRA','SDF','MID','MNSR','BYT','KSX','KPV','LD','WAB','VGN','BIX','GTT','MPI','BON','KLYT','PKU','NS','MNE','BEY','REN','BBM','PRR','BQU','SOG','ASN','KTHD','BLDI','BIO','SANR','DHRR','SLF','BJ','GII','YLG','PC','ATL','ATNR','BPZ','PPW','ABLE','KTM','RGS','KCJ','CNK','IGP','BPP','BLX','BXP','DOE','BHTR','GB','LNR','BOR','TGN','WANI','SOD','BLDA','KAD','BURN','JJK','KSW','WPR','MKDI','KOV','SHNR','JNR','KRH','BSKH','BNKI','PFM','JJR','ADT','UDGR','WDM','GPD','BXHT','BNY','BNP','SBV','JSG','JSGR','CM','BWI','RRS','BHKD','CLD','TDU','KAJG','VYA','MAQ','TVG','BRZ','EDN','JMKT','BALU','MAJN','SSR','MAGH','SZR','VBW','SNGP','BHT','NRT','RBS','SWE','KED','SWV','MEP','BGSF','KPGM','GUD','LUSA','CNS','ROI','GRH','TRT','BTH','RE','CWDA','DZA','FBG','BORD','KMS','DARA','GRKN','GKH','VEER','JNA','BRKA','HLKT','SPQ','BBTR','CTND','TL','PLY','BLW','LLR','KBM','TKBG','MK','JWO','HRG','JPD','GRCP','PPC','MGG','GDV','ROA','BDW','BCU','CHTL','BGTA','DMM','DEOR','KNNK','PNDM','KL','CBN','GND','MSDH','GNK','BHLE','WRR','BOKR','KPNA','ODB','NBH','GVI','HVD','DIB','GCH','MGN','GAP','RUM','ARV','PYD','DAS','BG','JGJN','NB','SMRR','VLT','TLHR','HSRA','DHA','NMG','CAER','BKO','JRU','SLO','POU','PBM','KLT','RGU','PHK','MHO','KEPR','BZLE','DGI','DAB','RRME','SELU','CH','MQR','RMNP','PKPU','NGY','BXN','DKO','WIRR','POY','ANGL','DOL','BKP','MHPE','SGUJ','GUG','HDK','NHH','SBBJ','CMW','TDD','DSS','NRE','PUU','DBA','KMBL','MBY','VPDA','JID','CDA','PEM','TELO','TKQ','GHGL','PTKP','NRW','BINR','TGQ','TGRL','TMX','CRWA','MDW','ANDN','HPO','JGA','SD','BPK','SNN','NJP','MAI','KYE','RBK','SKS','JAL','SBIB','SBT','KHED','CUX','RNR','JMK','RBD','PTRU','SHR','TLD','LUNI','DGU','NKK','MZM','BLD','VR','KRNR','SLKR','ARW','PSLI','AGMN','BTU','BNVD','SAV','KKGM','NAW','DES','BN','SL','CGR','KO','KIP','MEH','KUE','MGAE','GDYA','SFA','BWM','KSV','SVRP','KNL','KKNA','TGU','TNKU','BSDP','MV','AKT','LHA','JGM','MIM','ULT','BRR','NWH','NDN','KPO','NH','LHU','LMT','GJD','PMK','MXH','DL','WSJ','RMT','MJRI','ULL','SRBA','PTH','RSR','MDP','CHV','OPL','KSH','MME','HMG','PCH','CHZ','CPP','DAA','RAG','KMME','KWO','AFR','GVR','OEA','ALB','GDR','BSE','RFJ','MJL','CKS','PERN','GDL','BUT','STJT','AHQ','HPLE','NMGA','BMR','BOD','VNA','CLJ','SKGH','TIW','ATRU','STNL','ABS','YA','CPN','STN','BRAG','ADR','KLJ','BLPU']
        #non_working = 
        
        working = []
        
        for z in h:
            t = z.strip("\n")
            working.append(t)
    

        for x in f:
            t = x.split(" ")
            g.write("ZZZZ\n"+t[0]+" ")
            #print("\n"+t[0])
            
            
            for z in t:
                t1 = z.split(",")
                try:
                    #print(t1[1])
                    if t1[0] in working:
                        #print(z)
                        g.write(z+" ")
                except:
                    continue              
                
        g.write('ZZZZ\n')
        
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@22
def calc_length_of_new_routes():
        f = open('new_routes_with_distances.txt','r')
        g = open('new_routes_lengths.txt','w')
        
        c=0
        no_s = 0
        for x in f:
            if (c==0):
                c = c+1
                continue
            
            t = x.split(" ")
            try:
                
                if(t[1]=='ZZZZ\n' or t[2]=='ZZZZ\n'):
                    continue
            except:
                pass
            g.write("\n"+t[0])
            #print(t[0])
            
            for c in range(1,200):
                try:
                    if (t[c] == 'ZZZZ\n') :
                        c = c-1
                        break
                    else:
                        q=t[c].split(",")[0]
                        g.write(" "+q)
                        
                except:
                    pass
                    
            try:
                
                b = t[1].split(",")[1]
                a = t[c].split(",")[1]
                d = int(a)-int(b)
                #print(int(a)-int(b))
                
            
                g.write(" "+str(d))
          
            except:
                 no_s= no_s + 1         
                 

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def only_minimun_length_routes():
    
##########Reversing in order to bring length at first place##########
        
        g = open('reversed_new_routes_lengths.txt','w')
        for x in reversed(list(open('new_routes_lengths.txt'))):
            words = x.split()
            reversed_words= ' '.join(reversed(words))
            g.write(reversed_words+"\n")
    
     
        

#############Taking only the routes length of which is greater than 100km.##########
        len = min_r_len
        f = open('reversed_new_routes_lengths.txt','r')
        g = open('reversed_new_routes_lengths_greaterthan100km.txt','w')
        for x in f:
            try:
                t = x.split(" ")
                if(int(t[0]) > int(len)):
                    g.write(x)
            except:
                pass
                    
#################Reversing again ##############################
        g = open('Re_reversed_new_routes_lengths.txt','w')
        for x in reversed(list(open('reversed_new_routes_lengths_greaterthan100km.txt'))):
            words = x.split()
            reversed_words= ' '.join(reversed(words))
            g.write(reversed_words+"\n")
                 


########################Removing empty lines from Hotspots.txt
def rem_emp_lines():
    with open('Hotspots.txt', 'r+') as fd:
        lines = fd.readlines()
        fd.seek(0)
        fd.writelines(line for line in lines if line.strip())
        fd.truncate()


#####################################MAPS####################################################
def maps():
    
    f = open('app/static/openstreetmaps/test/final/code_coordinates.txt','r')
    g = open('Working.txt','r')
    h = open('app/static/openstreetmaps/test/final/coordinates.txt','w')
    #i = open('names.txt','w')        
    working = []
    for z in g:
        t = z.strip("\n")
        working.append(t)
    
    c =0
    for x in f:
        t  = x.split(" ")
        if(t[0] in working):
            c = c+1    
            h.write(t[1])
            
    f.close()
    g.close()
    h.close()
            
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2
    f = open('app/static/openstreetmaps/test/final/code_names.txt','r')
    g = open('Working.txt','r')
    h = open('app/static/openstreetmaps/test/final/names.txt','w')
    #i = open('names.txt','w')        
    working = []
    for z in g:
        t = z.strip("\n")
        working.append(t)
    
    
    c = 0
    for x in f:
        t  = x.split(",")
        if(t[0] in working):
            c = c+1    
            h.write(t[0]+" "+t[1])
     
    f.close()
    g.close()
    h.close()
            
      #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    
    f = open('app/static/openstreetmaps/test/final/code_nac.txt','r')
    g = open('Working.txt','r')
    h = open('app/static/openstreetmaps/test/final/nac.txt','w')
    #i = open('names.txt','w')        
    working = []
    for z in g:
        t = z.strip("\n")
        working.append(t)
    
    c = 0
    for x in f:
        t  = x.split(" ")
        if(t[0] in working):
            c = c+1    
            h.write(t[1])
           
    f.close()
    g.close()
    h.close()
            
              
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@222
    l = []
    n=[]
    a = []
    
    h = open('app/static/openstreetmaps/test/final/coordinates.txt','r')
    g= open('app/static/openstreetmaps/test/final/names.txt','r')
    q = open('app/static/openstreetmaps/test/final/nac.txt','r')
    
    
    
    for z in h:
        t = z.strip("\n")
        l.append(t)
    
    for z in g:
        t = z.strip("\n")
        n.append(t)
    
    
    for z in q:
        t = z.strip("\n")
        a.append(t)
    
    
    f= open('app/static/openstreetmaps/test/final/Working_Stations_circle.txt','w')
    x=1
    for i,j,k in zip(l,n,a):
         f.write('var circle'+str(x)+' = L.circle(['+i+'], 100, {'+"\n"+'color: \'black\','+"\n"+'fillColor: \'#000000\','+"\n"+'fillOpacity: 0.9'+"\n"+'}).addTo(map);'+"\n\n")
         f.write('circle'+str(x)+'.bindPopup(\"<b>'+j+ '</b><br>'+k+'\");'+"\n\n\n\n")
         x = x+1
         
         
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@22
    
    
    f= open('app/static/openstreetmaps/test/final/3in1.html','w')
    
    g = open('app/static/openstreetmaps/test/final/top.txt','r')
    h = open('app/static/openstreetmaps/test/final/Working_Stations_circle.txt','r')
    q = open('app/static/openstreetmaps/test/final/bottom.txt','r')
    
    
    for x in g:
        f.write(x)
        
    f.write("\n\n")
        
    for x in h:
        f.write(x)
        
        
    f.write("\n\n")    
    
    for x in q:
        f.write(x)
        
        
    ####################################################################3
