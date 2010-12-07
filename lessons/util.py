def _check_markdown_cache(lesson, force=False):
  '''
  Check if the cache file exists for this lesson.
  If not, create one with the results of Markdown processing.
  The "cache file" means the resulting HTML content of the
  Markdown source of the lesson.
  '''
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
    # process with Markdown
    cache_content = markdown.markdown(lesson.content)
    cache_output = codecs.open(cache_file, 'wU', 'utf-8')
    cache_output.write(cache_content)
    cache_output.close()
  # now the HTML file should exist
  # build the template file name to be included in the template
  markdown_template = 'cache/%s' % markdown_template
  return markdown_template
