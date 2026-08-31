# frozen_string_literal: true

require "jekyll"
require "tmpdir"

source = File.expand_path("..", __dir__)

Dir.mktmpdir("flypython-render-security") do |destination|
  config = Jekyll.configuration(
    "source" => source,
    "destination" => destination,
    "quiet" => true,
    "disable_disk_cache" => true
  )
  site = Jekyll::Site.new(config)
  site.reset
  site.read

  path = site.data.fetch("resources").fetch("catalog").fetch("paths").first
  path["title_en"] = "<img src=x onerror=alert(1)>"
  path["title_zh"] = "<img src=x onerror=alert(1)>"
  path["summary_en"] = "<svg onload=alert(2)>"
  path["summary_zh"] = "<svg onload=alert(2)>"

  resource = site.data.fetch("resources").fetch("resources").first
  resource["title"] = "</a><script>alert(3)</script>"
  resource["why_en"] = "<math href=x onmouseover=alert(4)>"
  resource["why_zh"] = "<math href=x onmouseover=alert(4)>"
  resource["url"] = 'https://example.com/" onmouseover="alert(5)'

  site.generate
  site.render
  site.cleanup
  site.write

  html = ["index.html", File.join("zh", "index.html")].map do |relative_path|
    File.read(File.join(destination, relative_path), encoding: "UTF-8")
  end.join("\n")

  forbidden = [
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(2)>",
    "</a><script>alert(3)</script>",
    "<math href=x onmouseover=alert(4)>",
    'href="https://example.com/" onmouseover="alert(5)"'
  ]
  leaked = forbidden.select { |payload| html.include?(payload) }
  abort "unescaped catalog payloads: #{leaked.join(', ')}" unless leaked.empty?

  expected = [
    "&lt;img src=x onerror=alert(1)&gt;",
    "&lt;svg onload=alert(2)&gt;",
    "&lt;/a&gt;&lt;script&gt;alert(3)&lt;/script&gt;",
    "&lt;math href=x onmouseover=alert(4)&gt;",
    "https://example.com/&quot; onmouseover=&quot;alert(5)"
  ]
  missing = expected.reject { |payload| html.include?(payload) }
  abort "escaped catalog payloads missing: #{missing.join(', ')}" unless missing.empty?
end

puts "catalog output escaping valid"
