# -*- coding: utf-8 -*-
"""
regexes:[a-z]+ 
[A-Z]+  
[A-Za-z]+ 
[0-9]+ 
[a-zA-Z0-9]+ 
[a-z]+[0-9]+ 
[a-zA-Z]+[0-9]+
[a-zA-Z]+1
[a-zA-Z]+!
[a-zA-Z]+1! 
[0-9]+[a-zA-Z]+ 
[0-9]+[a-z]+
"""


import re
import tables as t
from xxhash import xxh32_intdigest
import os




#Debugging and folder presets
DEBUG = True
sources = [i for i in range(9)]
RDIR = "e:/Diplomska/leaks/f9"
all_dirs = os.listdir(RDIR)


pseps = [':', ';', ' ', ',', '_', '::', ';;', '  ', '__', '..', ',,', '|']
    
mail_basic_pat = r"[^ @\t\n\r\f\v]+@[^ @\t\n\r\f\v]+\.[^ @\t\n\r\f\v]+"
mail_basic_checker = re.compile(mail_basic_pat)
#mail_bullshit_pat = r"[^ @\t\n\r\f\v]*@[^ @\t\n\r\f\v]*[\.,]*[^ @\t\n\r\f\v]*"
#mail_bullshit_checker = re.compile(mail_bullshit_pat)
hash_pat = r"[a-fA-F0-9]+"
hash_checker = re.compile(hash_pat)


h5file = t.open_file("e:/Diplomska/BThesis.h5", 'a')
table = h5file.root.C1.f9
pswd = table.row
#h5file.enable_undo()

def corrector(l):
    return "".join(l.split())


for source in sources:
    DIRNAME = all_dirs[source]
    PATHNAME = RDIR + '/' + DIRNAME
    files = os.listdir(PATHNAME)
    dumps_path = "e:/diplomska/OTHERS/" + DIRNAME
    
    #Too long section
    hashes = 0
    dashes = 0 #weird 'hashes' that have a dash after ~8 chars and use a-Z
    numeric = 0 #consisting completly of digits
    emails = 0 #consisting of concatenated email addresses
    others = 0 #everything that does not fit the above categories and can be analyzed later
    
    #Other counts
    hashpicious = 0 #all the passwords in the form of a hash e.g. (32 chars and hash_pat regex)
    emails2 = 0 #all the passwords that also have the form of an email.
    unascii = 0 #all the passwords that do not contain ascii chars
    no_emails = 0 #lines where no email/valid pswd was found
    working = 0 #all the pswds that escaped the filtering system above
    #mrk = h5file.mark("BEG")
    print(f"Starting folder {DIRNAME}")
    
    try:      
        for fname in files:
            ln = 0
            #mrk = h5file.mark(fname)
            with open(PATHNAME + '/' + fname, "r", encoding='utf-8', errors = 'ignore') as file:
                #try:
                    for l in file:
                        ln += 1
                        line = l.strip('\n" ')
                        
                        
                        line = corrector(line)
                        
                        if len(line) <5:
                            continue
                        
                        
                        works = False
                        works1 = False
                        works2 = False
        
                        two_emails= False
                                        
                        
                        for s in pseps:
                            try:
                                p1, p2 = line.split(s, maxsplit = 1)
                                
                                
                                check1 = mail_basic_checker.fullmatch(p1)
                                check2 = mail_basic_checker.fullmatch(p2)
                                
                                if check1 and check2:
                                    two_emails = True
                                    break
                                
                                elif check1:
                                    works = True
                                    ps = p2
                                    break
                                
                                elif check2:
                                    works = True
                                    ps = p1
                                    break
                            
                            except ValueError:
                                continue
                            
                            
                        
                        if two_emails:
                            emails2 += 1
                            if DEBUG:
                                with open(dumps_path + "___2EMAILS___.txt", 'a', encoding = 'utf-8') as dump:
                                    dump.write(line + '\n')
                            continue
                        
                        if not works:
                            no_emails += 1
                            if DEBUG:
                                with open(dumps_path + "___WEIRD___.txt", 'a', encoding = 'utf-8') as dump:
                                    dump.write(line + '\n')
                            continue
                            
            
                        try:
                            byt = ps.encode('ascii')
                        except UnicodeEncodeError:
                            unascii += 1
                            if DEBUG:
                                with open(dumps_path + "___UNASCII___.txt", 'a', encoding = 'utf-8') as dump:
                                            dump.write(ps + '\n')
                            continue
                        
                        if len(ps) == 32 and hash_checker.fullmatch(ps):
                            
                            hashpicious += 1
                            if DEBUG:
                                with open(dumps_path + "___HASHES___.txt", 'a', encoding = 'utf-8') as dump:
                                    dump.write(ps + '\n')
                            continue
                        
                        elif "$HEX" in ps:
                            if DEBUG:
                                with open(dumps_path + "___SQL___.txt", 'a', encoding = 'utf-8') as dump:
                                    dump.write(ps + '\n')
                            continue
                        
                        elif len(ps) > 64:
                            if hash_checker.fullmatch(ps):
                                hashes +=1
                            
                            elif '-' in ps:
                                dashes += 1
                            
                            elif '@' in ps:
                                emails += 1
                            
                            elif ps.isdigit():
                                numeric += 1
                            
                            else:
                                others += 1
                                if DEBUG:
                                    with open(dumps_path + "___TROP___.txt", 'a', encoding = 'utf-8') as dump:
                                        dump.write(ps + '\n')
                            continue
                            
                        elif len(ps) == 0:
                            continue
                        
                        """
                        found = False
                        hsh = xxh32_intdigest(ps)
                        query = [r for r in table.where(f"xhashx == {hsh}")]
                        if len(query) >= 1:
                            for r in query:
                                if r['password'] == ps:
                                    r['src'] |= 1
                                    r['cnt'] += 1
                                    found = True
                                    break
                                    
                        if not found:"""
                        pswd['xhashx'] = xxh32_intdigest(ps)
                        pswd["password"] = ps
                        pswd['src'] = 1 << source
    
                        pswd.append()
                        
                        working += 1
                #except UnicodeDecodeError:
                    
                    
            table.flush()
            #os.remove(DIRNAME + '/' +  fname)
    
    except:
        print("calling except")
        table.flush()
        h5file.close()
        #h5file.goto("BEG")
        raise
    finally:
        tl = emails + numeric + hashes + dashes + others    
        dumpd = emails2 + no_emails + unascii + hashpicious
        
        with open(dumps_path + "___STATS___.txt", 'a') as st:
            st.write(f"total lines: {dumpd + working + hashpicious + tl}\n\
                       working: {working}\n\
                       hashpicious passwords: {hashpicious}\n\
                       TOTAL tl: {tl}; concatenated emails: {emails}; digits: {numeric}, dashed: {dashes}, hashes: {hashes}, others: {others}\n\
                       dumpd_TOTAL: {dumpd}, 2emails: {emails2}, no emails: {no_emails}, not ascii: {unascii}\n")
            
        with open(dumps_path + "___STATS___.csv", 'a') as st:
            st.write(f"{dumpd + working + hashpicious + tl}\n\
                       {working}\n\
                       {hashpicious}\n\
                       {tl},{emails},{numeric},{dashes},{hashes},{others}\n\
                       {dumpd},{emails2},{no_emails},{unascii}\n")
        
        
        print(f"Ending folder {DIRNAME}")

                    
           
    
h5file.close()
                     
            
        
            
            
            
            
            
            


