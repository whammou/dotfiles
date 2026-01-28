function RawBlock(rawblock)
	if rawblock.format:match("html") then
		local srcPattern = '<img%ssrc="([^"]+)".*/>'
		local scalePattern = "<img.*:%s?(%d+%%).*/>"
		local src = string.match(rawblock.text, srcPattern)
		local scale = string.match(rawblock.text, scalePattern)
		if src then
			return pandoc.Para(pandoc.Image({}, src, nil, { width = scale }))
		end
	end
end
