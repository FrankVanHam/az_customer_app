import os, datetime
import argparse
import xml.etree.ElementTree as ET

'''
This script converts magik test results XML files into a single NUnit format XML file.
It scans a given directory for XMLS and create one NUnit XML file as output.
'''
class XMLConverter:
    def __init__(self):
        pass
    
    def convert(self, path, target):
        xmls = []
        contents = os.listdir(path)
        for item in contents:
            item_path =  os.path.join(path, item)
            if os.path.isfile(item_path):
                if item_path.lower().endswith(".xml"):
                    print(f"Found XML file: {item_path}")
                    if os.stat(item_path).st_size > 0:
                        xml = self.convert_file(item_path)
                        if xml is not None:
                            xmls.append(xml)
        tree = self.combine_nunit_xmls(xmls)
        tree.write(target, encoding='utf-8', xml_declaration=True)
    
    def convert_file(self, xml_file):
        try:
            tree = ET.parse(xml_file)
            return tree.getroot()
        except Exception as e:
            print(f"Failed to parse XML file: {xml_file}")
            return None
        
    def combine_nunit_xmls(self, xmls):
        attrib = self.root_attributes()
        nunit_root = ET.Element('test-run', attrib)
        c = 0
        for xml in xmls:
            self.add_suite(nunit_root, c, xml)
            c += 1
        nunit_tree = ET.ElementTree(nunit_root)
        ET.indent(nunit_tree, space="  ", level=0)
        return nunit_tree

    def root_attributes(self):
        d = datetime.date.today()
        return {
            'name': 'root', 
            'id': '0',
            'run-date': d.strftime("%Y-%m-%d"),
            'start-time': d.strftime("%H:%M:%S")
            }
        
    def add_suite(self, nunit_root, count, magik_suite):
        attrib = self.suite_attributes(nunit_root, count, magik_suite)
        suite = ET.SubElement(nunit_root, "test-suite", attrib)
        c = 0
        for sub_suite in magik_suite.findall('testsuite'):
            self.add_suite(suite, c, sub_suite)
            c += 1
        c = 0
        for case in magik_suite.findall('testcase'):
            self.add_suite_case(suite, c, case)
            c += 1

    def suite_attributes(self, nunit_root, count, magik_suite):
        return {
            'type': "TestSuite",
            'id': nunit_root.attrib['id'] + '.' + str(count),
            'name': magik_suite.attrib['name'],
            'fullname': nunit_root.attrib['name'] +'/'+ magik_suite.attrib['name'],
            'testcasecount': magik_suite.get('tests', '0'),
            'result': "Failed" if int(magik_suite.attrib.get('failures', 0)) > 0 else "Passed",
            'time': magik_suite.attrib['time'], 
            'total': magik_suite.get('tests', '0'),
            'passed': str(int(magik_suite.get('tests', 0)) - int(magik_suite.get('failures', 0))),
            'failed': magik_suite.get('failures', '0')}

    def add_suite_case(self, suite, count, magik_case):
        attrib = self.suite_case_attributes(suite, count, magik_case)
        case = ET.SubElement(suite, "test-case", attrib)
        for failure in magik_case.findall('failure'):
            self.add_failure(case, failure)
    
    def suite_case_attributes(self, suite, count, magik_case):
        return {
            'id': suite.attrib['id'] + '.' + str(count),
            'name': magik_case.attrib['name'],
            'fullname': suite.attrib['name'] + '/' + magik_case.attrib['name'],
            'result': "Failed" if magik_case.attrib["status"] == 'Failed' else 'Passed',
            'time' : magik_case.attrib['time']}

    def add_failure(self, case, magik_failure):
        attrib = {}
        failure = ET.SubElement(case, "failure", attrib)
        failure_text = ET.SubElement(failure, "message")
        failure_text.text = magik_failure.text

def main():
    parser = argparse.ArgumentParser("convert_magik_xml_to_nunit_xml.py converts magik test results into one NUnit format XML.")
    parser.add_argument("path", help="The path to scan for magik XML", type=str)
    parser.add_argument("target", help="The target filename NUnit to create", type=str)
    args = parser.parse_args()
    
    path = os.path.abspath(args.path)
    target = os.path.abspath(args.target)
    
    converter = XMLConverter()
    results = converter.convert(path, target)

if __name__ == "__main__":
    main()