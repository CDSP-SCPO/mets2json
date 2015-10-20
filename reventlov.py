#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Libs
#
import codecs, json, logging, os
import xml.etree.ElementTree as ET

#
# Config
#
folder_separator = '/'
log_folder = 'log'
log_file = log_folder + folder_separator + 'reventlov.log'
log_level = logging.DEBUG
data_folder = 'data'
data_input = data_folder + folder_separator + 'cdsp_bequali_sp5.xml'
data_output = data_folder + folder_separator + 'reventlov.json'

#
# Programm
#
'''
Convert a METS document in XML format into a MetaJSON format.
This MetaJSON format will be used by the website to display the informations about this survey.
'''
def main():
	# Import and parse XML file
	logging.info('Import file')
	tree = ET.parse(data_input)
	logging.info('File uploaded')
	root = tree.getroot()
	namespaces = {
		'ddi': 'ddi:codebook:2_2',
		'dc' : 'http://purl.org/dc/elements/1.1/'
	}
	# Create result variable
	data = {}

	# spatialunits : codeBook/stdyDscr/stdyInfo/sumDscr/geogUnit
	# multiple
	s = []
	for value in root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:sumDscr/ddi:geogUnit", namespaces) :
		s.append(value.text.encode('utf8'))
	data['coverage_spatial_units'] = s

	# locationofunitsofobservation : codeBook/stdyDscr/stdyInfo/sumDscr/universe
	# get only the second element
	s = root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:sumDscr/ddi:universe", namespaces)[1].text
	data['location_of_units_of_observations'] = s

	# targetgroups : codeBook/stdyDscr/stdyInfo/sumDscr/universe
	# get only the fourth element
	s = root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:sumDscr/ddi:universe", namespaces)[3].text
	data['target_groups'] = s

	# observunits : codeBook/stdyDscr/stdyInfo/sumDscr/analyUnit
	# multiple
	s = []
	for value in root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:sumDscr/ddi:anlyUnit", namespaces) :
		s.append(value.text.encode('utf8'))
	data['observation_units'] = s

	# geogcover : codeBook/stdyDscr/stdyInfo/sumDscr/geogCover
	# multiple
	s = []
	for value in root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:sumDscr/ddi:geogCover", namespaces) :
		s.append(value.text.encode('utf8'))
	data['coverage_spatial_geographics'] = s

	# langdoc
	# multiple
	s = set([])
	for value in root.findall(".//dc:identifier", namespaces) :
		if any(ext in value.text.split('_')[3] for ext in ['ana', 'anal', 'prep', 'pre']) :
			s.add(value.text.split('_')[6].encode('utf8'))
	s = ';'.join(s)
	# TODO
	data['documentation_languages'] = [s] if s != '' else []

	# langdata
	# multiple 
	s = set([])
	for value in root.findall(".//dc:identifier", namespaces) :
		if value.text.split('_')[3] == 'col' :
			s.add(value.text.split('_')[6])
	s = ';'.join(s)
	#TODO
	data['data_languages'] = [s] if s != '' else []

	# transcription : codeBook/stdyDscr/stdyInfo/sumDscr/dataKind
	# multiple
	s = []
	for value in root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:sumDscr/ddi:dataKind", namespaces) :
		if value.get('type') is None :
			s.append(value.text.encode('utf8'))
	data['analysis_transcription'] = s

	# anonymization : codeBook/stdyDscr/stdyInfo/notes
	# 0 if not present in the XML, 1 else
	s = len(root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:notes", namespaces))
	if s != 0 :
		s = 1
	data['analysis_anonymization'] = s

	# analysis : codeBook/stdyDscr/stdyInfo/notes
	# multiple
	# empty array if not present in the XML
	s = []
	for value in root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:notes", namespaces) :
		s.append(value.text.encode('utf8'))
	data['analysis_types'] = s

	# discipline : codeBook/stdyDscr/stdyInfo/subject/topcClas
	# multiple
	s = []
	for value in root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:subject/ddi:topcClas", namespaces) :
		s.append(value.text.encode('utf8'))
	data['disciplines'] = s

	# titl : codeBook/stdyDscr/citation/titlStmt/titl
	s = root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:citation/ddi:titlStmt/ddi:titl", namespaces).text
	data['title'] = s.encode('utf8')

	# abstract : codeBook/stdyDscr/stdyInfo/abstract
	# multiple
	s = []
	for value in root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:abstract", namespaces) :
		s.append(value.text.encode('utf8'))
	data['descriptions'] = s

	# nation : codeBook/stdyDscr/stdyInfo/sumDscr/nation
	# multiple
	s = []
	for value in root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:sumDscr/ddi:nation", namespaces) :
		s.append(value.text.encode('utf8'))
	data['coverage_spatial_countries'] = s

	# idno : codeBook/stdyDscr/citation/titlStmt/IDNo
	s = root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:citation/ddi:titlStmt/ddi:IDNo", namespaces).text
	data['rec_id'] = s

	# keywords : codeBook/stdyDscr/stdyInfo/subject/keyword
	# multiple
	s = []
	for value in root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:subject/ddi:keyword", namespaces) :
		s.append(value.text.encode('utf8'))
	# TODO
	# keywords[language][i]
	data['keywords'] = s

	# timeperiodcovered : codeBook/stdyDscr/stdyInfo/sumDscr/timePrd@start
	start = root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:sumDscr/ddi:timePrd[@event='start']", namespaces).text
	data['coverage_temporal_begin'] = start
	# timeperiodcovered : codeBook/stdyDscr/stdyInfo/sumDscr/timePrd@end
	end = root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:sumDscr/ddi:timePrd[@event='end']", namespaces).text
	data['coverage_temporal_end'] = end

	# copyright : codeBook/docDscr/citation/prodStmt/copyright
	# multiple
	s = ''
	for value in root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:citation/ddi:prodStmt/ddi:copyright", namespaces) :
		if s != '' :
			s += ';'
		s += value.text.encode('utf8')
	# TODO
	# copyright_holders[i].rec_class=Person,
	# copyright_holders[i].name_family,
	# copyright_holders[i].name_given,
	# copyright_holders[i].affiliations[i].rec_class=Orgunit,
	# copyright_holders[i].affiliations[i].name
	# copyright_holders[i].rec_class=Orgunit,
	# copyright_holders[i].name

	# locarch : codeBook/stdyDscr/dataAccs/setAvail/origArch
	s = root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:dataAccs/ddi:setAvail/ddi:origArch", namespaces).text
	data['archive_location'] = s

	# accessconditions : codeBook/stdyDscr/dataAccs/useStmt/condition
	# multiple
	s = []
	for value in root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:dataAccs/ddi:useStmt/ddi:condition", namespaces) :
		s.append(value.text.encode('utf8'))
	data['access_conditions'] = s

	# editor : codeBook/docDscr/citation/rspStmt/AuthEnty
	# multiple
	s = ''
	for value in root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:citation/ddi:rspStmt/ddi:AuthEnty", namespaces) :
		if s != '' :
			s += ';'
		s += value.text.encode('utf8')
	# TODO
	# editors[i].rec_class=Person,
	# editors[i].name_family,
	# editors[i].name_given,
	# editors[i].affiliations[i].rec_class=Orgunit,
	# editors[i].affiliations[i].name
	# editors[i].rec_class=Orgunit,
	# editors[i].name

	# latestedition : codeBook/docDscr/citation/verStmt/version@date
	s = root.find(".//ddi:codeBook/ddi:docDscr/ddi:citation/ddi:verStmt", namespaces)
	data['edition_last_date'] = s.attrib['date']

	# software : codeBook/docDscr/citation/prodStmt/software
	# multiple
	s = []
	for value in root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:citation/ddi:prodStmt/ddi:software", namespaces) :
		s.append(value.text.encode('utf8'))
	data['softwares'] = s

	# distrbtr : codeBook/stdyDscr/citation/distStmt/distrbtr
	# multiple
	s = ''
	for value in root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:citation/ddi:distStmt/ddi:distrbtr", namespaces) :
		if s != '' :
			s += ';'
		s += value.text.encode('utf8')
	# TODO
	# distributors[i].rec_class=Person,
	# distributors[i].name_family,
	# distributors[i].name_given,
	# distributors[i].affiliations[i].rec_class=Orgunit,
	# distributors[i].affiliations[i].name
	# distributors[i].rec_class=Orgunit,
	# distributors[i].name

	# authenty : codeBook/stdyDscr/citation/rspStmt/AuthEnty
	# multiple
	s = []
	for value in root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:citation/ddi:rspStmt/ddi:AuthEnty", namespaces) :
		t = {}
		t['name'] = value.text.encode('utf8')
		t['affiliation'] = value.attrib['affiliation']
		s.append(t)
	# TODO
	# authors[i].rec_class=Person,
	# authors[i].name_family,
	# authors[i].name_given,
	# authors[i].affiliations[i].rec_class=Orgunit,
	# authors[i].affiliations[i].name
	# authors[i].rec_class=Orgunit,
	# authors[i].name

	# grantno : codeBook/stdyDscr/citation/prodStmt/grantNo
	# multiple
	s = ''
	for value in  root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:citation/ddi:prodStmt/ddi:grantNo", namespaces) :
		if s != '' :
			s += ';'
		s += value.text.encode('utf8')
	# TODO
	# projects[i].acronym
	# projects[i].title
	# projects[i].funding_agency.rec_class=Orgunit,
	# projects[i].funding_agent.name
	# projects[i].identifiers[i].value

	# fundag : codeBook/stdyDscr/citation/prodStmt/fundAg
	# multiple
	s = ''
	for value in  root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:citation/ddi:prodStmt/ddi:fundAg", namespaces) :
		if s != '' :
			s += ';'
		s += value.text.encode('utf8')
	# TODO
	# cf. above "grantno"

	# numberoffiles : codeBook/stdyDscr/dataAccs/setAvail/fileQnty
	s = root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:dataAccs/ddi:setAvail/ddi:fileQnty", namespaces).text
	data['documents_count'] = s.encode('utf8')

	# datakind : codeBook/stdyDscr/stdyInfo/sumDscr/dataKind@type
	# multiple
	s = []
	for value in root.findall(".//ddi:stdyInfo/ddi:sumDscr/ddi:dataKind", namespaces) :
		if value.get('type'):
			s.append(value.text.encode('utf8'))
	data['data_collection_documents_types'] = s

	# methodofdatacollection : codeBook/stdyDscr/method/dataColl/resInstru
	# multiple
	s = []
	for value in root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:method/ddi:dataColl/ddi:resInstru", namespaces) :
		s.append(value.text.encode('utf8'))
	data['data_collection_methods'] = s

	# colldate : codeBook/stdyDscr/stdyInfo/sumDscr/collDate
	start = root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:sumDscr/ddi:collDate[@event='start']", namespaces).text
	data['data_collection_date_begin'] = start
	end = root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:sumDscr/ddi:collDate[@event='end']", namespaces).text
	data['data_collection_date_end'] = end

	# modedatacollection : codeBook/stdyDscr/method/dataColl/collMode
	# multiple
	s = []
	for value in root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:method/ddi:dataColl/ddi:collMode", namespaces) :
		s.append(value.text.encode('utf8'))
	data['data_collection_modes'] = s

	# timedimension : codeBook/stdyDscr/method/dataColl/timeMeth
	# multiple
	s = []
	for value in root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:method/ddi:dataColl/ddi:timeMeth", namespaces) :
		s.append(value.text.encode('utf8'))
	data['data_collection_time_dimensions'] = s

	# sampprocedure : codeBook/stdyDscr/method/dataColl/sampProc
	# multiple
	s = []
	for value in root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:method/ddi:dataColl/ddi:sampProc", namespaces) :
		s.append(value.text.encode('utf8'))
	data['data_collection_samplings'] = s

	# Write result into file
	with codecs.open(data_output, 'w', 'utf8') as f:
		f.write(json.dumps(data, ensure_ascii=False, indent=4).decode('utf8'))
	f.close()
	logging.info('End')

#
# Main
#
if __name__ == '__main__':
	# Check that log folder exists, else create it
	if not os.path.exists(log_folder):
		os.makedirs(log_folder)
	logging.basicConfig(filename = log_file, filemode = 'w', format = '%(asctime)s  |  %(levelname)s  |  %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p', level = log_level)
	logging.info('Start')
	main()