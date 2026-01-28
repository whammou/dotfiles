function RawBlock(rawblock)
	if rawblock.format:match("html") then
		local srcPattern = '<img%ssrc="([^"]+)".*/>'
		local scalePattern = "<img.*:%s?(%d+%%).*/>"
		local src = string.match(rawblock.text, srcPattern)
		local scale = string.match(rawblock.text, scalePattern)
		if src then
			local image_inline = pandoc.Image({}, src, nil, { width = scale })
			local para_block = pandoc.Para({ image_inline })
			return {
				pandoc.RawBlock("tex", "\\centering"),
				para_block,
				pandoc.RawBlock("tex", "\\par"),
			}
		end
	end
end
