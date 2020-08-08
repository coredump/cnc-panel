#!/usr/bin/env ruby

require 'nokogiri'

schem = File.open('Plan.qet') { |f| Nokogiri::XML(f) }

elems = schem.xpath('//dynamic_elmt_text//text[contains(text(),"X")]').select { |e| e.text =~ /X\d:/ }
        .each do |z|
    
    k = schem.at_xpath(z.parent.path)
    k['font'] = "Sans Serif,7,-1,5,0,0,0,0,0,0,normal"
end

puts schem.to_xml
