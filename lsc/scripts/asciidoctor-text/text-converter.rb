# adoc to plaintext converter plugin for asciidoctor
#

module Asciidoctor
  class Converter::TextConverter < Converter::Base
    register_for 'text'

    def convert(node, transform = node.node_name, opts = nil)
      case transform
      when 'document'
        convert_document(node)
      when 'section'
        convert_section(node)
      when 'paragraph'
        node.content
      when 'ulist'
        convert_ulist(node)
      when 'olist'
        convert_olist(node)
      when 'dlist'
        convert_dlist(node)
      when 'list_item'
        convert_list_item(node)
      when 'image'
        "![#{node.attr('alt')}]"
      when 'literal'
        decode(node.content)
      when 'quote'
        "> #{node.content}"
      when 'verse'
        "```\n#{node.content}\n```"
      when 'floating_title'
        convert_floating_title(node)
      when 'admonition'
        convert_admonition(node)
      when 'listing'
        convert_listing(node)
      else
        handle_unknown_node(node)
      end
    end

    private

    def convert_document(node)
      result = []
      result << "# " + decode(node.doctitle) if node.header?
      result << node.blocks.map { |child| convert(child) }.join("\n\n")
      result.join("\n\n")
    end

    def convert_section(node)
      result = []
      result << "#{('#' * node.level)} " + decode(node.title)
      result << node.blocks.map { |child| convert(child) }.join("\n\n")
      result.join("\n\n")
    end

    def convert_ulist(node)
      node.items.map { |item| "* #{convert(item)}" }.join("\n")
    end

    def convert_olist(node)
      node.items.each_with_index.map { |item, index| "#{index + 1}. #{convert(item)}" }.join("\n")
    end

    def convert_dlist(node)
      node.items.map { |(terms, descs)|
        convert_dlist_terms_and_descs(terms, descs)
      }.join("\n")
    end

    def convert_dlist_terms_and_descs(terms, descs)
      terms_text = terms.map { |term| decode(term.text) }.join(", ")
      descs_text = (convert(descs) if not descs.nil?) || ""
      "#{terms_text}:: #{descs_text}"
    end

    def convert_list_item(node)
      content = (decode(node.text) if not node.text.nil?) || ""
      if node.blocks?
        node.blocks.each do |block|
          if block.title?
            content += "\n" + decode(block.title)
          end
          if block.context == :paragraph
            content += "\n\n#{convert(block)}"
          elsif block.context == :literal
            content += "\n\n#{convert(block)}"
          else
            content += "\n#{convert(block)}"
          end
        end
      end
      content
    end

    def convert_floating_title(node)
      "## " + decode(node.title)
    end

    def convert_admonition(node)
      type = node.attr('name').upcase
      content = node.content
      decode("\n[#{type}]\n----\n#{content}\n----\n")
    end

    def convert_listing(node)
      language = node.attr('language')
      content = node.content
      ret = "\n```"
      if language
        ret += decode(language)
      end
      ret += "\n#{decode(content)}\n```\n"
    end

    def handle_unknown_node(node)
      if node.respond_to?(:content)
        if node.content.is_a?(Array)
          node.content.map { |child| convert(child) }.join("\n")
        else
          decode(node.content)
        end
      elsif node.respond_to?(:text)
        decode(node.text)
      else
        ""
      end
    end

    def decode str
      unless str.nil?
        str = str.
          gsub('&lt;', '<').
          gsub('&gt;', '>').
          gsub('&#43;', '+').     # plus sign; alternately could use \c(pl
          gsub('&#160;', ' ').    # non-breaking space
          gsub('&#174;', '(R)').  # registered trademark
          gsub('&#8201;', ' ').   # thin space
          gsub('&#8211;', '-').   # en dash
          gsub('&#8212;', '-').   # em dash
          gsub('&#8216;', %(')).  # left single quotation mark
          gsub('&#8217;', %(')).  # right single quotation mark
          gsub('&#8220;', %(")).  # left double quotation mark
          gsub('&#8221;', %("")). # right double quotation mark
          gsub('&#8592;', '<-').  # leftwards arrow
          gsub('&#8594;', '->').  # rightwards arrow
          gsub('&#8656;', '->').  # leftwards double arrow
          gsub('&#8658;', '<-').  # rightwards double arrow
          gsub('&amp;', '&').     # literal ampersand (NOTE must take place after any other replacement that includes &)
          gsub('\'', %(')).       # apostrophe / neutral single quote
          rstrip                  # strip trailing space
        end
      str
    end

  end
end
