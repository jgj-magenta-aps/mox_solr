sudo  su -l -c 'solr-7.7.0/bin/solr delete -c os2mo-employee' donald
sudo  su -l -c 'solr-7.7.0/bin/solr create -c os2mo-employee' donald
sudo  su -l -c 'solr-7.7.0/bin/solr delete -c os2mo-orgunit' donald
sudo  su -l -c 'solr-7.7.0/bin/solr create -c os2mo-orgunit' donald

