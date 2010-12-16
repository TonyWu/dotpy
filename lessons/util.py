sub_title_list = []

def _replace_lesson_sub_title(match):
  """
  Replace the current sub title of the lesson with new one:
  add the "id" attribute and "top" link.
  Parameter match: the match object.
  """
  global sub_title_list
  sub_id = 'lesson_sub_title_%s' % len(sub_title_list)
  sub_title = match.group(1)
  sub_title_list.append((sub_id, sub_title))
  return '<h2 id="%s">%s <span class="navtop"><a href="#lesson-subject">[Top]</a></span></h2>' \
          %s (sub_id, sub_title)

def _gen_table_of_contents_for_lesson(content):
  """
  Generate the table of contents for the given lesson
  content (HTML) and return the full content
  """
  import re
  global sub_title_list # TODO
  pattern = r'<h2>(\w+)</h2>'
  new_content = re.sub(pattern, _replace_lesson_sub_title, content)
  if sub_title_list:
    table_of_contents = '''
      <div id="nav">
        <table class="unruled">
          <tr>
            <td class="first">
              <dl>
    '''
    per_column_num = math.ceil(len(sub_title_list))
    if per_column_num < 7:
      per_column_num = 7
    _count = 1
    for sub_item in sub_title_list:
      _mod = _count % per_column_num
      if _mod == 0:
        table_of_contents += '</dl></td>'
      elif _mod == 1 and _count != 1:
        table_of_contents += "<td><dl>"
      _item = '<dt><a href="#%s">%s</a></dt>' % sub_item
      table_of_contents += _item
    if len(sub_title_list) % per_column_num != 0:
      table_of_contents += '</dl></td>'
    return '%s\n%s' % (table_of_contents, new_content)
  else: # sub_title_list
    return new_content

def _escape_template_tags(content):
  return content.replace('{', '{%templatetag openbrace%}')

def check_lesson_markdown_cache(lesson, force=False):
  """
  Check if the cache file exists for this lesson.
  If not, create one with the results of Markdown processing.
  The "cache file" means the resulting HTML file of the
  Markdown source of the lesson.
  """
  import os
  from os import path
  base_dir = path.abspath(path.dirname(__file__))
  # first, check the cache directory
  cache_dir = path.join(base_dir, 'templates/cache/')
  if not path.exists(cache_dir):
    os.mkdir(cache_dir)
  markdown_template = '%s.html' % lesson.slug
  cache_file = path.join(cache_dir, markdown_template)
  # now check the cache file, if not exist, create it
  if force or not path.exists(cache_file):
    import markdown
    import codecs
    # generate HTML with Markdown
    cache_content = markdown.markdown(lesson.content)
    # generate the table of contents
    cache_content = _gen_table_of_contents_for_lesson(cache_content)
    # do NOT forget to replace Django template tags
    cache_content = _escape_template_tags(cache_content)
    # wirte into file
    cache_output = codecs.open(cache_file, 'w', 'utf8')
    cache_output.write(cache_content)
    cache_output.close()
  # now the HTML file should exist
  # build the template file name to be included in the template
  markdown_template = 'cache/%s' % markdown_template
  return markdown_template
