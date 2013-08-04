import os
from collections import defaultdict

# VPC Template
vpctemplate = '''
//-----------------------------------------------------------------------------
//	PYSOURCE_AUTOGEN.VPC
//
//	Project Script
//-----------------------------------------------------------------------------

$Macro SRCDIR		"..\.."

$Project
{
	$Folder	"Source Files"
	{
		$Folder	"Python"
		{
			$Folder	"Modules"
			{
				$Folder	"AutoGenerated"
				{
%(Content)s
				}
			}
		}
	}
}
'''

filtertemplate = '''					$Folder	"%(FilterName)s"
					{
%(Content)s
					}
'''

def GenerateVPCs(settings, filepaths, outpath):
    # Create content with filenames
    content = ''
    filters = defaultdict(str)
    
    for path in filepaths:
        basepath, filtername = path.split(settings.autogenfoldername)
        filtername = os.path.dirname(filtername).lstrip('\\')
        if filtername:
            filters[filtername] += '\t\t\t\t\t\t$File	"$SRCDIR\%s"\n' % (path)
        else:
            content += '\t\t\t\t\t$File	"$SRCDIR\%s"\n' % (path)
            
    for filter, filtercontent in filters.items():
        content += filtertemplate % {'FilterName' : filter, 'Content' : filtercontent}
        
    # Write out file using the template
    with open(outpath, 'wb') as fp:
        content = vpctemplate % {'Content' : content}
        fp.write(bytes(content, 'utf-8'))
       
    