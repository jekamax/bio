header='''LOCUS       region [166800000 168200000] annotations                06-DEC-2020
UNIMARK     region [166800000 168200000] annotations
FEATURES             Location/Qualifiers'''

featureTemplate='''
     misc_binding    {ugene_positions}
                     /ugene_name="{ugene_name}"
                     /ugene_group="factors_from_ensemble"
                     /factors="{feature[factors]}"
                     /epigenes="{feature[epigenomes]}"'''

footer='''
//
'''

def dump_genbank(features):
    content=header
    for feature in features:
        ugene_positions=f"{feature['file_start']}..{feature['file_end']}"
        ugene_name=feature['id']
        content+=featureTemplate.format_map(locals())
    content+=footer
    return content;
        
