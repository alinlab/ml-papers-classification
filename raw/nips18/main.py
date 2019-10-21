#!/usr/bin/python
import os
import re
import urllib2

def find_string_position(input, start_str, end_str):
    start_pattern = re.compile(start_str)
    end_pattern = re.compile(end_str)
    if start_pattern.search(input) == None:
        return -1,-1
    s1 = start_pattern.search(input).end()
    s2 = end_pattern.search(input, s1).start()
    return s1,s2

url_name = 'https://nips.cc/Conferences/2018/Schedule?bySubject=&selectedSubject='

filename = "html_nips.txt"
fid = open(filename, 'r')
contents = fid.read()
fid.close()

sid = 1;
cnt = 1;
endflag = 0;
while(1):
    s1,s2 = find_string_position(contents, 'value="', '"')
    if s1 == -1:
        break
    r1,r2 = find_string_position(contents, '">', ' </label>')

    id = contents[s1:s2]
    cat_name = contents[r1:r2]
    cat_name = cat_name.replace(" ","_")
    cat_name = cat_name.replace(",","")
    cat_name = cat_name.replace("/","_")
    if 'Components' in cat_name:
        cat_name = 'Components_Analysis'
    cat_html = cat_name + '.html'
    print('[{:3}] id = {:4}, name = {:}'.format(sid, id, cat_name))


    os.system("mkdir -p ./subject/" + cat_name)
    if os.path.isfile("./subject/" + cat_name + "/" + cat_html) == False:
        os.system("wget -O " + "./subject/" + cat_name + "/" + cat_html + " \"" + url_name + str(id) + "\"")


    fname = "./subject/" + cat_name + "/" + cat_html
    fid2 = open(fname, 'r')
    content_sub = fid2.read()
    fid2.close()

    while(1):
        t1,t2 = find_string_position(content_sub, '<div class="maincardBody">', '</div>')
        if t1==-1:
            break
        title = content_sub[t1:t2]
        title = title.replace(" ","_")
        title = title.replace(",","")
        title = title.replace(":_",":")
        title = title.replace("-","_")
        title = title.replace("''","")
        print("[{:<3}] title = {:10}".format(cnt,'./subject/'+cat_name + '/' + title + '.pdf'))
        cnt += 1

        y1, y2 = find_string_position(content_sub, '<span class="maincard_media maincard_media_PDF">\n                    <a href="http://papers.nips', '" class=')
        plink = 'http://papers.nips' + content_sub[y1:y2]
        content_sub = content_sub[y2+1:]

        if os.path.isfile("./subject/" + cat_name + "/" + title + ".pdf") == True:
            continue

        # if cnt < 511:
        #     continue
        # import pdb; pdb.set_trace()

        # print(plink)
        os.system("wget -q -O " + "tmp.html " + plink)

        fid2 = open("tmp.html", 'r')
        content_tmp = fid2.read()
        fid2.close()
        z1,z2 = find_string_position(content_tmp, '<meta name="citation_pdf_url" content="', '">')
        paper_url = content_tmp[z1:z2]

        # print("paper url = " + paper_url)
        try:
            req = urllib2.urlopen(plink)
            plink = req.geturl()
            plink = plink + '.pdf'
        except:
            import pdb; pdb.set_trace()
            if title == 'Differentially_Private_Change_Point_Detection':
                plink = 'http://papers.nips.cc/paper/8280-differentially-private-change-point-detection.pdf'
            elif title == 'Point_process_latent_variable_models_of_larval_zebrafish_behavior':
                plink = 'http://papers.nips.cc/paper/8289-point-process-latent-variable-models-of-larval-zebrafish-behavior.pdf'
            elif title == 'Learning_Hierarchical_Semantic_Image_Manipulation_through_Structured_Representations':
                plink = 'http://papers.nips.cc/paper/7536-learning-hierarchical-semantic-image-manipulation-through-structured-representations.pdf'
            elif title == 'Reward_learning_from_human_preferences_and_demonstrations_in_Atari':
                plink = 'http://papers.nips.cc/paper/8025-reward-learning-from-human-preferences-and-demonstrations-in-atari.pdf'
            else:
                import pdb; pdb.set_trace()


        if os.path.isfile("./subject/" + cat_name + "/" + title + ".pdf") == False:
            os.system("wget -O ./subject/" + cat_name + "/" + title + ".pdf " + plink)

    contents = contents[r2+1:]
    sid += 1
