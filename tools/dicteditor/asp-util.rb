
def to_lower(str)
	cmd = IO.popen("echo \"#{str}\" | LC_ALL=uk_UA.UTF-8 awk '{ print tolower($0) }'", mode: 'r+:UTF-8')
	res = cmd.gets
    cmd.close
	return res.chop
end
