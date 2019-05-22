#! /usr/bin/env python3

import vcf
import httplib2
import json

__author__ = 'XXX'

currentVCF = '../data/chr16.vcf'


##
##
## Aim of this assignment is to annotate the variants with various attributes
## We will use the API provided by "myvariant.info" - more information here: https://docs.myvariant.info
## NOTE NOTE! - check here for hg38 - https://myvariant.info/faq
## 1) Annotate the first 900 variants in the VCF file
## 2) Store the result in a data structure (not in a database)
## 3) Use the data structure to answer the questions
##
## 4) View the VCF in a browser
##

class Assignment3:
    
    def __init__(self, i_VCF):
        ## Check if pyvcf is installed
        print("PyVCF version: %s" % vcf.VERSION)
        
        ## Call annotate_vcf_file here
        self.vcf_path = i_VCF  # TODO

    def annotate_vcf_file(self):
        '''
        - Annotate the VCF file using the following example code (for 1 variant)
        - Iterate of the variants (use first 900)
        - Store the result in a data structure
        :return:
        '''    

        ##
        ## Example loop
        ##
        
        ## Build the connection
        h = httplib2.Http()
        headers = {'content-type': 'application/x-www-form-urlencoded'}
                
        params_pos = []  # Generate a list of the first 900 variant positions occuring in input VCF File
        with open(self.vcf_path) as my_vcf_fh:
            vcf_reader = vcf.Reader(my_vcf_fh)
            for counter, record in enumerate(vcf_reader):
                params_pos.append(record.CHROM + ":g." + str(record.POS) + record.REF + ">" + str(record.ALT[0]))

                if counter >= 899:
                    break
        
        ## Build the parameters using the list we just built
        params = 'ids=' + ",".join(params_pos) + '&hg38=true'

        ## Perform annotation
        res, con = h.request('http://myvariant.info/v1/variant', 'POST', params, headers=headers)
        annotation_result = con.decode('utf-8')

        ## TODO now do something with the 'annotation_result'
        
        ##
        ## End example code
        ##
        # Convert output json string to a list of dictionaries?
        o_AnnotationDataset = json.loads(annotation_result) #

        return o_AnnotationDataset  ## return the data structure here
                                        ## was ist mit datastructure gemeint?
    
    
    def get_list_of_genes(self, i_AnnotationDataset):
        '''
        Print the name of genes in the annotation data set
        :return:
        '''
        oList_genesAnnotated = []
        for subDict in i_AnnotationDataset:
            if 'cadd' in subDict.keys(): # überseh ich da sachen? eg dnsnp annotation
                oList_genesAnnotated.append(subDict['cadd']['gene'])

        return oList_genesAnnotated
    
    
    def get_num_variants_modifier(self, i_AnnotationDataset):
        #Print the number of variants with putative_impact "MODIFIER"
        nVariant = 0
        for line in i_AnnotationDataset:
            line = str(line)
            if line.find("'putative_impact': 'MODIFIER'") != -1:
                nVariant +=1
        return nVariant
    
    def get_num_variants_with_mutationtaster_annotation(self, i_AnnotationDataset):
        #Print the number of variants with a 'mutationtaster' annotation

        nVariant = 0
        for line in i_AnnotationDataset:
            line = str(line)
            if line.find("'mutationtaster'") != -1:
                nVariant += 1
        return nVariant
        
    
    def get_num_variants_non_synonymous(self, i_AnnotationDataset):
        '''
        Print the number of variants with 'consequence' 'NON_SYNONYMOUS'
        :return:
        '''
        nVariant = 0
        for line in i_AnnotationDataset:
            line = str(line)
            if line.find("'consequence' 'NON_SYNONYMOUS'") != -1:
                nVariant += 1
        return nVariant
        
    
    def view_vcf_in_browser(self):
        '''
        - Open a browser and go to https://vcf.iobio.io/
        - Upload the VCF file and investigate the details
        :return:
        '''
   
        ## Document the final URL here
        print("TODO")
            
    
    def print_summary(self):
        annotationDataset = self.annotate_vcf_file()
        annotatedGenes = self.get_list_of_genes(annotationDataset)
        print("Number of Variants modifying putative impact:\t%s " % (self.get_num_variants_modifier(annotationDataset)))
        print("Number of Variants with mutationtaster annotation:\t%s "  % (self.get_num_variants_with_mutationtaster_annotation(annotationDataset)))
        print("Number of Variants with non-synonymous mutations:\t %s " % (self.get_num_variants_non_synonymous(annotationDataset)))
        self.view_vcf_in_browser()

    
def main():
    print("Assignment 3")
    assignment3 = Assignment3(currentVCF)
    assignment3.print_summary()
    print("Done with assignment 3")
        
        
if __name__ == '__main__':
    main()
   
    



