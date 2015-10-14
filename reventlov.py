#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Libs
#
import codecs, io, json, logging, sys
import xml.etree.ElementTree as ET

#
# Config
#
folderSeparator = '/'
logFolder = 'log'
logFile = logFolder + folderSeparator + 'reventlov.log'
logLevel = logging.DEBUG
dataFolder = 'data'
dataInput = dataFolder + folderSeparator + 'cdsp_bequali_sp5.xml'
dataOutput = dataFolder + folderSeparator + 'reventlov.json'

#
# Programm
#
logging.basicConfig(filename = logFile, filemode = 'w', format = '%(asctime)s  |  %(levelname)s  |  %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p', level = logLevel)
logging.info('Start')

'''
Convert a METS document in XML format into a MetaJSON format.
This MetaJSON format will be used by the website to display the informations about this survey.
'''
def main():
	# Import and parse XML file
	logging.info('Import file')
	tree = ET.parse(dataInput)
	logging.info('File uploaded')
	root = tree.getroot()
	namespaces = {
		'ddi': 'ddi:codebook:2_2',
		'dc' : 'http://purl.org/dc/elements/1.1/'
	}
	# Create result variable
	# data = {}
	# data['label'] = {}
	# data['label']['langdoc'] = 'Langage documentation'
	# data['label']['locationofunitsofobservation'] = 'Niveau de comparatisme'
	# data['label']['abstract'] = 'Résumé'
	# data['label']['general'] = 'Général'
	# data['label']['affiliation'] = 'Affiliation'
	# data['label']['keywords'] = 'Mots clefs'
	# data['label']['copyright'] = 'copyright'
	# data['label']['discipline'] = 'Discipline'
	# data['label']['methodofdatacollection'] = 'Technique de collection'
	# data['label']['titl'] = 'Nom'
	# data['label']['actor'] = 'Acteur(s)'
	# data['label']['targetgroups'] = 'Groupes de population ciblés'
	# data['label']['collsitu'] = 'Durée des observations'
	# data['label']['accessconditions'] = 'Conditions d\'accès'
	# data['label']['contact'] = 'Contact'
	# data['label']['colldate'] = 'Dates de récolte des données'
	# data['label']['anonymization'] = 'Anonymisation'
	# data['label']['corpus'] = 'Corpus'
	# data['label']['authenty'] = 'Auteur(s)'
	# data['label']['sampprocedure'] = 'Echantillonnage '
	# data['label']['distrbtr'] = 'Distributeur'
	# data['label']['description'] = 'Description'
	# data['label']['topicclassification'] = 'Classification'
	# data['label']['nation'] = 'Pays'
	# data['label']['timedimension'] = 'Périodicité'
	# data['label']['modedatacollection'] = 'Accès aux observations'
	# data['label']['numberofunits'] = 'Nombre d\'observations'
	# data['label']['studydates'] = 'Dates de l\'enquête'
	# data['label']['timeperiodcovered'] = 'Période couverte'
	# data['label']['spatialunits'] = 'Unités spatialisées'
	# data['label']['datakind'] = 'Types de documents'
	# data['label']['weighting'] = 'Segmentation'
	# data['label']['edition'] = 'Edition'
	# data['label']['universe'] = 'Univers'
	# data['label']['numberoffiles'] = 'Nombre de documents'
	# data['label']['locarch'] = 'Localisation archives'
	# data['label']['analysis'] = 'Analyse'
	# data['label']['method'] = 'Méthode'
	# data['label']['grantno'] = 'Bourse'
	# data['label']['idno'] = 'DDI Id'
	# data['label']['observunits'] = 'Unités d\'observation'
	# data['label']['langdata'] = 'Language données'
	# data['label']['editor'] = 'Edition'
	# data['label']['geogcover'] = 'Couverture géographique'
	# data['label']['transcription'] = 'Transcription'
	# data['label']['fundag'] = 'Agence de financement'
	# data['label']['latestedition'] = 'Dernière version'
	# data['label']['software'] = 'Logiciel'

	## universe
	# data['values'] = {}
	# data['values']['universe'] = {}
	# data['values']['universe']['i'] = 2

	# spatialunits : codeBook/stdyDscr/stdyInfo/sumDscr/geogUnit
	# multiple
	s = ''
	for value in root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:sumDscr/ddi:geogUnit", namespaces) :
		if s != '' :
			s += ';'
		s += value.text
	# data['values']['universe']['spatialunits'] = {}
	# data['values']['universe']['spatialunits']['i'] = 2
	# data['values']['universe']['spatialunits']['value'] = [s]
	data['coverage_spatial_units'] = [s]

	# locationofunitsofobservation : codeBook/stdyDscr/stdyInfo/sumDscr/universe
	# multiple
	# get only the second element
	s = root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:sumDscr/ddi:universe", namespaces)[1].text
	# data['values']['universe']['locationofunitsofobservation'] = {}
	# data['values']['universe']['locationofunitsofobservation']['i'] = 0
	# data['values']['universe']['locationofunitsofobservation']['value'] = [s]
	data['location_of_units_of_observations'] = [s]

	# targetgroups : codeBook/stdyDscr/stdyInfo/sumDscr/universe
	# multiple
	# get only the fourth element
	s = root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:sumDscr/ddi:universe", namespaces)[3].text
	# data['values']['universe']['target_groups'] = {}
	# data['values']['universe']['target_groups']['i'] = 0
	# data['values']['universe']['target_groups']['value'] = [s]
	data['target_groups'] = [s]

	# observunits : codeBook/stdyDscr/stdyInfo/sumDscr/analyUnit
	# multiple
	s = ''
	for value in root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:sumDscr/ddi:anlyUnit", namespaces) :
		if s != '' :
			s += ';'
		s += value.text.encode('utf8')
	# data['values']['universe']['observunits'] = {}
	# data['values']['universe']['observunits']['i'] = 3
	# data['values']['universe']['observunits']['value'] = [s]
	data['observation_units'] = [s]

	# geogcover : codeBook/stdyDscr/stdyInfo/sumDscr/geogCover
	# multiple
	s = ''
	for value in root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:sumDscr/ddi:geogCover", namespaces) :
		if s != '' :
			s += ';'
		s += value.text.encode('utf8')
	# data['values']['universe']['geogcover'] = {}
	# data['values']['universe']['geogcover']['i'] = 1
	# data['values']['universe']['geogcover']['value'] = [s]
	data['coverage_spatial_geographics'] = [s]

	# studydates : codeBook/stdyDscr/stdyInfo/sumDscr/timePrd
	start = root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:sumDscr/ddi:timePrd[@event='start']", namespaces).text
	data['coverage_temporal_begin'] = [start]

	end = root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:sumDscr/ddi:timePrd[@event='end']", namespaces).text
	# data['values']['universe']['timeperiodcovered'] = {}
	# data['values']['universe']['timeperiodcovered']['i'] = 5
	# data['values']['universe']['timeperiodcovered']['value'] = [start + '-' + end]
	data['coverage_temporal_end'] = [end]

	## analysis
	# data['values']['analysis'] = {}
	# data['values']['analysis']['i'] = 5

	# langdoc
	# multiple
	s = set([])
	for value in root.findall(".//dc:identifier", namespaces) :
		if any(ext in value.text.split('_')[3] for ext in ['ana', 'anal', 'prep', 'pre']) :
			s.add(value.text.split('_')[6].encode('utf8'))
	s = ';'.join(s)
	# data['values']['analysis']['langdoc'] = {}
	# data['values']['analysis']['langdoc']['i'] = 4
	# data['values']['analysis']['langdoc']['value'] = [s]
	data['documentation_languages'] = [set]

	# langdata
	# multiple 
	s = set([])
	for value in root.findall(".//dc:identifier", namespaces) :
		if value.text.split('_')[3] == 'col' :
			s.add(value.text.split('_')[6])
	s = ';'.join(s)
	# data['values']['analysis']['langdata'] = {}
	# data['values']['analysis']['langdata']['i'] = 0
	# data['values']['analysis']['langdata']['value'] = [s]
	data['data_languages'] = [s]

	# transcription : codeBook/stdyDscr/stdyInfo/sumDscr/dataKind
	# multiple
	s = ''
	for value in root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:sumDscr/ddi:dataKind", namespaces) :
		if value.get('type') is None :
			s += value.text
	# data['values']['analysis']['transcription'] = {}
	# data['values']['analysis']['transcription']['i'] = 0
	# data['values']['analysis']['transcription']['value'] = [s]
	data['analysis_transcription'] = [s]

	# anonymization : codeBook/stdyDscr/stdyInfo/notes
	# 0 if not present in the XML, 1 else
	s = len(root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:notes", namespaces))
	if s != 0 :
		s = 1
	# data['values']['analysis']['anonymization'] = {}
	# data['values']['analysis']['anonymization']['i'] = 1
	# data['values']['analysis']['anonymization']['value'] = [s]
	data['analysis_anonymization'] = [s]

	# analysis : codeBook/stdyDscr/stdyInfo/notes
	# multiple
	# empty if not present in the XML
	s = ''
	for value in root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:notes", namespaces) :
		if s != '' :
			s += ';'
		s += value.text
	# data['values']['analysis']['analysis'] = {}
	# data['values']['analysis']['analysis']['i'] = 2
	# data['values']['analysis']['analysis']['value'] = [s]
	data['analysis_types'] = [s]

	## general
	# data['values']['general'] = {}
	# data['values']['general']['i'] = 0

	# discipline : codeBook/stdyDscr/stdyInfo/subject/topcClas
	# multiple
	s = ''
	for value in root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:subject/ddi:topcClas", namespaces) :
		if s != '' :
			s += ';'
		s += value.text
	# data['values']['general']['topicclassification'] = {}
	# data['values']['general']['topicclassification']['i'] = 4
	# data['values']['general']['topicclassification']['value'] = [s]
	data['disciplines'] = [s]

	# titl : codeBook/stdyDscr/citation/titlStmt/titl
	s = root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:citation/ddi:titlStmt/ddi:titl", namespaces).text
	# data['values']['general']['titl'] = {}
	# data['values']['general']['titl']['i'] = 1
	# data['values']['general']['titl']['value'] = [s.encode('utf8')]
	data['title'] = [s.encode('utf8')]

	# abstract : codeBook/stdyDscr/stdyInfo/abstract
	# multiple
	s = ''
	for value in root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:abstract", namespaces) :
		if s != '' :
			s += ';'
		s += value.text
	# data['values']['general']['abstract'] = {}
	# data['values']['general']['abstract']['i'] = 3
	# data['values']['general']['abstract']['value'] = [s.encode('utf8')]
	# TODO
	data['descriptions'] = [s.encode('utf8')]

	# nation : codeBook/stdyDscr/stdyInfo/sumDscr/nation
	# multiple
	s = ''
	for value in root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:sumDscr/ddi:nation", namespaces) :
		if s != '' :
			s += ';'
		s += value.text
	# data['values']['general']['nation'] = {}
	# data['values']['general']['nation']['i'] = 7
	# data['values']['general']['nation']['value'] = [s]
	data['coverage_spatial_countries'] = [s]

	# idno : codeBook/stdyDscr/citation/titlStmt/IDNo
	s = root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:citation/ddi:titlStmt/ddi:IDNo", namespaces).text
	# data['values']['general']['idno'] = {}
	# data['values']['general']['idno']['i'] = 0
	# data['values']['general']['idno']['value'] = [s]
	data['rec_id'] = [s]

	# keywords : codeBook/stdyDscr/stdyInfo/subject/keyword
	# multiple
	s = ''
	for value in root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:subject/ddi:keyword", namespaces) :
		if s != '' :
			s += ';'
		s += value.text
	# data['values']['general']['keywords'] = {}
	# data['values']['general']['keywords']['i'] = 5
	# data['values']['general']['keywords']['value'] = [s]
	# keywords[language][i]
	data['keywords'] = [s]

	# timeperiodcovered : codeBook/stdyDscr/stdyInfo/sumDscr/timePrd@start
	start = root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:sumDscr/ddi:timePrd[@event='start']", namespaces).text
	data['coverage_temporal_begin'] = start
	end = root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:sumDscr/ddi:timePrd[@event='end']", namespaces).text
	data['coverage_temporal_end'] = end
	# data['values']['general']['timeperiodcovered'] = {}
	# data['values']['general']['timeperiodcovered']['i'] = 8
	# data['values']['general']['timeperiodcovered']['value'] = [start + '-' + end]

	## edition
	# data['values']['edition'] = {}
	# data['values']['edition']['i'] = 6

	# copyright : codeBook/docDscr/citation/prodStmt/copyright
	# multiple
	s = ''
	for value in root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:citation/ddi:prodStmt/ddi:copyright", namespaces) :
		if s != '' :
			s += ';'
		s += value.text
	# data['values']['edition']['copyright'] = {}
	# data['values']['edition']['copyright']['i'] = 4
	# data['values']['edition']['copyright']['value'] = [s]
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
	# data['values']['edition']['locarch'] = {}
	# data['values']['edition']['locarch']['i'] = 2
	# data['values']['edition']['locarch']['value'] = [s]
	data['archive_location'] = [s]

	# accessconditions : codeBook/stdyDscr/dataAccs/useStmt/condition
	# multiple
	s = ''
	for value in root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:dataAccs/ddi:useStmt/ddi:condition", namespaces) :
		if s != '' :
			s += ';'
		s += value.text
	# data['values']['edition']['accessconditions'] = {}
	# data['values']['edition']['accessconditions']['i'] = 0
	# data['values']['edition']['accessconditions']['value'] = [s.encode('utf8')]
	data['access_conditions'] = [s.encode('utf8')]

	# editor : codeBook/docDscr/citation/rspStmt/AuthEnty
	# multiple
	s = ''
	for value in root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:citation/ddi:rspStmt/ddi:AuthEnty", namespaces) :
		if s != '' :
			s += ';'
		s += value.text
	# data['values']['edition']['editor'] = {}
	# data['values']['edition']['editor']['i'] = 6
	# data['values']['edition']['editor']['value'] = [s.encode('utf8')]
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
	# data['values']['edition']['latestedition'] = {}
	# data['values']['edition']['latestedition']['i'] = 3
	# data['values']['edition']['latestedition']['value'] = [s.attrib['date']]
	data['edition_last_date'] = [s.attrib['date']]

	# software : codeBook/docDscr/citation/prodStmt/software
	# multiple
	s = ''
	for value in root.findall(".//ddi:codeBook/ddi:stdyDscr/ddi:citation/ddi:prodStmt/ddi:software", namespaces) :
		if s != '' :
			s += ';'
		s += value.text
	# data['values']['edition']['software'] = {}
	# data['values']['edition']['software']['i'] = 5
	# data['values']['edition']['software']['value'] = [s]
	data['softwares'] = [s]

	## actor
	# data['values']['actor'] = {}
	# data['values']['actor']['i'] = 1

	# distrbtr : codeBook/stdyDscr/citation/distStmt/distrbtr
	# multiple
	s = ''
	for value in root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:citation/ddi:distStmt/ddi:distrbtr", namespaces) :
		if s != '' :
			s += ';'
		s += value.text
	# data['values']['actor']['distrbtr'] = {}
	# data['values']['actor']['distrbtr']['i'] = 2
	# data['values']['actor']['distrbtr']['value'] = [s]
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
	# data['values']['actor']['authenty'] = {}
	# data['values']['actor']['authenty']['i'] = 0
	# data['values']['actor']['authenty']['value'] = s
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
		s += value.text
	# data['values']['actor']['grantno'] = {}
	# data['values']['actor']['grantno']['i'] = 4
	# data['values']['actor']['grantno']['value'] = [s]
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
		s += value.text
	# data['values']['actor']['fundag'] = {}
	# data['values']['actor']['fundag']['i'] = 4
	# data['values']['actor']['fundag']['value'] = [s]
	# TODO
	# cf. above "grantno"

	## corpus
	# data['values']['corpus'] = {}
	# data['values']['corpus']['i'] = 4

	# numberofunits : codeBook/stdyDscr/method/dataColl/deviat
	# deprecated

	# numberoffiles : codeBook/stdyDscr/dataAccs/setAvail/fileQnty
	s = root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:dataAccs/ddi:setAvail/ddi:fileQnty", namespaces).text
	# data['values']['actor']['numberoffiles'] = {}
	# data['values']['actor']['numberoffiles']['i'] = 3
	# data['values']['actor']['numberoffiles']['value'] = [s.encode('utf8')]
	data['documents_count'] = [s.encode('utf8')]

	# collsitu : codeBook/stdyDscr/method/dataColl/collSitu
	# deprecated

	# datakind : codeBook/stdyDscr/stdyInfo/sumDscr/dataKind@type
	# multiple
	s = ''
	for value in root.findall(".//ddi:stdyInfo/ddi:sumDscr/ddi:dataKind", namespaces) :
		if value.get('type'):
			s += value.text
	# data['values']['actor']['datakind'] = {}
	# data['values']['actor']['datakind']['i'] = 1
	# data['values']['actor']['datakind']['value'] = [s]
	data['data_collection_documents_types'] = [s]

	## method
	data['values']['method'] = {}
	data['values']['method']['i'] = 3

	# methodofdatacollection : codeBook/stdyDscr/method/dataColl/resInstru
	# multiple
	s = ''
	for value in root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:method/ddi:dataColl/ddi:resInstru", namespaces) :
		if s != '' :
			s += ';'
		s += value.text
	# data['values']['actor']['methodofdatacollection'] = {}
	# data['values']['actor']['methodofdatacollection']['i'] = 5
	# data['values']['actor']['methodofdatacollection']['value'] = [s]
	data['data_collection_methods'] = [s]

	# colldate : codeBook/stdyDscr/stdyInfo/sumDscr/collDate
	start = root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:sumDscr/ddi:collDate[@event='start']", namespaces).text
	data['data_collection_date_begin'] = start
	end = root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:stdyInfo/ddi:sumDscr/ddi:collDate[@event='end']", namespaces).text
	data['data_collection_date_end'] = end
	# data['values']['actor']['colldate'] = {}
	# data['values']['actor']['colldate']['i'] = 0
	# data['values']['actor']['colldate']['value'] = [start + '-' + end]

	# weighting
	# deprecated

	# modedatacollection : codeBook/stdyDscr/method/dataColl/collMode
	# multiple
	s = ''
	for value in root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:method/ddi:dataColl/ddi:collMode", namespaces) :
		if s != '' :
			s += ';'
		s += value.text
	# data['values']['actor']['modedatacollection'] = {}
	# data['values']['actor']['modedatacollection']['i'] = 2
	# data['values']['actor']['modedatacollection']['value'] = [s.encode('utf8')]
	data['data_collection_modes'] = [s.encode('utf8')]

	# timedimension : codeBook/stdyDscr/method/dataColl/timeMeth
	# multiple
	s = ''
	for value in root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:method/ddi:dataColl/ddi:timeMeth", namespaces) :
		if s != '' :
			s += ';'
		s += value.text
	# data['values']['actor']['timedimension'] = {}
	# data['values']['actor']['timedimension']['i'] = 1
	# data['values']['actor']['timedimension']['value'] = [s]
	data['data_collection_time_dimensions'] = [s]

	# sampprocedure : codeBook/stdyDscr/method/dataColl/sampProc
	# multiple
	s = ''
	for value in root.find(".//ddi:codeBook/ddi:stdyDscr/ddi:method/ddi:dataColl/ddi:sampProc", namespaces) :
		if s != '' :
			s += ';'
		s += value.text
	# data['values']['actor']['sampprocedure'] = {}
	# data['values']['actor']['sampprocedure']['i'] = 3
	# data['values']['actor']['sampprocedure']['value'] = [s.encode('utf8')]
	data['data_collection_samplings'] = [s.encode('utf8')]

	# Write result into file
	with codecs.open(dataOutput, 'w', 'utf8') as f:
		f.write(json.dumps(data, ensure_ascii=False, indent=4).decode('utf8'))
	f.close()

if __name__ == '__main__':
	main()