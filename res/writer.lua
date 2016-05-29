-- a part of mearie.org

-- we don't want to run unit tests every time pandoc process the data.
-- a console version of `lua` gives a table value for `arg`,
-- so we only run the tests when `arg` is set to the table.
local unitTests
local addUnitTest
if type(arg) == 'table' then
    unitTests = {}
    addUnitTest = function(f) table.insert(unitTests, f) end
else
    addUnitTest = function(f) end
end

--------------------------------------------------------------------------------

function table.equal(a, b)
    for k, va in pairs(a) do
        local vb = rawget(b, k)
        local tva, tvb = type(va), type(vb)
        if tva ~= tvb then return false end
        if not (rawequal(va, vb) or (tva == 'table' and table.equal(va, vb))) then
            return false
        end
    end
    for k, vb in pairs(b) do
        local va = rawget(a, k)
        local tva, tvb = type(va), type(vb)
        if tva ~= tvb then return false end
        -- since equality is reflexive, it's enough to check that
        -- every element in b is in a. (but it is possible that va *is* nil.)
    end
    return true
end
addUnitTest(function()
    assert(table.equal({}, {}))
    assert(table.equal({1, 2, 3}, {1, 2, 3}))
    assert(table.equal({a='b'}, {a='b'}))
    assert(table.equal({a='b', c=42}, {c=42, a='b'}))
    assert(table.equal({a='b', c=nil}, {a='b'}))
    assert(table.equal({a='b', 7}, {7, a='b'}))
    assert(table.equal({a='b'}, {c=nil, a='b'}))
    assert(table.equal({a={b={c='d'}}}, {a={b={c='d'}}}))
    assert(not table.equal({1, 2, 3}, {3, 2, 1}))
    assert(not table.equal({a='b'}, {a='c'}))
    assert(not table.equal({a='b\0c'}, {a='b\0d'}))
    assert(not table.equal({a='b'}, {a=42}))
    assert(not table.equal({a='b', c=42}, {a='b'}))
    assert(not table.equal({a='b'}, {a='b', c=42}))
    assert(not table.equal({a='b', c={}}, {a='b'}))
    assert(not table.equal({a='b'}, {a='b', c={}}))
    assert(not table.equal({a='b', 7}, {8, a='b'}))
    assert(not table.equal({a={b={c='d'}}}, {a={c={b='d'}}}))
end)

local ESCAPE_MAP = {
    ['<'] = '&lt;', ['>'] = '&gt;', ['&'] = '&amp;', ['"'] = '&quot;',
}
function string.escape(s)
    return s:gsub('[<>&"]', function(x) return ESCAPE_MAP[x] end)
end
addUnitTest(function()
    assert((''):escape() == '')
    assert(('<a href="foo">'):escape() == '&lt;a href=&quot;foo&quot;&gt;')
    assert(('?q=w&e=r&t=y'):escape() == '?q=w&amp;e=r&amp;t=y')
    assert(("let there be 'light'"):escape() == "let there be 'light'")
end)

local E = {}
do
    local function makeElement(tag, attrs, s)
        local ret = {'<' .. tag}
        if attrs then
            for k, v in pairs(attrs) do
                if type(k) == 'string' then
                    if v and #v > 0 then
                        table.insert(ret, ' ' .. k .. '="' .. v:escape() .. '"')
                    end
                else
                    -- nested attributes
                    for k, v in pairs(v) do
                        if v and #v > 0 then
                            table.insert(ret, ' ' .. k .. '="' .. v:escape() .. '"')
                        end
                    end
                end
            end
        end
        if s then
            table.insert(ret, '>')
            table.insert(ret, s)
            table.insert(ret, '</' .. tag .. '>')
        else
            table.insert(ret, ' />')
        end
        return table.concat(ret)
    end

    local meta = {}
    meta.__index = function(_, tag)
        return function(attrs)
            if type(attrs) == 'table' then
                return function(s) return makeElement(tag, attrs, s) end
            else
                return makeElement(tag, nil, attrs)
            end
        end
    end
    setmetatable(E, meta)
end
addUnitTest(function()
    assert(E.a() == '<a />')
    assert(E.a('b') == '<a>b</a>')
    assert(E.a('<b />') == '<a><b /></a>')
    assert(E.a{href=''}() == '<a />')
    assert(E.a{href='#'}() == '<a href="#" />')
    assert(E.a{href='<a href="#" />'}() == '<a href="&lt;a href=&quot;#&quot; /&gt;" />')
    assert(E.a{id='', href='#'}() == '<a href="#" />')
    do
        local s = E.a{id='foo', href='bar'}('what')
        assert(s == '<a id="foo" href="bar">what</a>' or
               s == '<a href="bar" id="foo">what</a>')
    end
end)

function string.encodepercent(s)
    return s:gsub('([^A-Za-z0-9_.~-])', function(c)
        return ('%%%02X'):format(c:byte(1))
    end)
end
addUnitTest(function()
    assert((''):encodepercent() == '')
    assert(('+_+'):encodepercent() == '%2B_%2B')
    assert((' al PHA b3t '):encodepercent() == '%20al%20PHA%20b3t%20')
    assert(('%'):encodepercent():encodepercent():encodepercent() == '%252525')
end)

function string.decodepercent(s)
    return s:gsub('%%([0-9a-fA-F][0-9a-fA-F])', function(c)
        return string.char(tonumber(c, 16))
    end)
end
addUnitTest(function()
    assert((''):decodepercent() == '')
    assert(('%2b%5F+'):decodepercent() == '+_+')
    assert(('%20al%20P%48A%20b3t%20'):decodepercent() == ' al PHA b3t ')
    assert(('%2'):decodepercent() == '%2')
    assert(('%cq'):decodepercent() == '%cq')
    assert(('%%25'):decodepercent() == '%%')
    assert(('%25252525'):decodepercent():decodepercent():decodepercent() == '%25')
    assert(('%2525252'):decodepercent():decodepercent():decodepercent() == '%2')
    assert(('%252525'):decodepercent():decodepercent():decodepercent() == '%')
    assert(('%25252'):decodepercent():decodepercent():decodepercent() == '%2')
    assert(('%2525'):decodepercent():decodepercent():decodepercent() == '%')
end)

function string.slashestopercent(s)
    return s:gsub('\\([^A-Za-z0-9_.~-])', function(c)
        return ('%%%02X'):format(c:byte(1))
    end)
end
addUnitTest(function()
    assert((''):slashestopercent() == '')
    assert(('\\n'):slashestopercent() == '\\n')
    assert(('\\\n'):slashestopercent() == '%0A')
    assert(('\\?'):slashestopercent() == '%3F')
    assert(('\\\\?'):slashestopercent() == '%5C?')
    assert(('\\\\\\?'):slashestopercent() == '%5C%3F')
end)

local function pipe(cmd, inp)
    local tmp = os.tmpname()
    local tmph = io.open(tmp, 'w')
    tmph:write(inp)
    tmph:close()
    local outh = io.popen(cmd .. ' ' .. tmp, 'r')
    local result = outh:read('*all')
    outh:close()
    os.remove(tmp)
    return result
end

local function hasClass(attrs, class)
    if attrs.class and (' ' .. attrs.class .. ' '):find(' ' .. class .. ' ', nil, true) then
        return true
    else
        return false
    end
end

local function makeGenSectionNumber()
    local sectionNumber = {}
    return function(currentLevel)
        assert(currentLevel >= 1)
        while currentLevel < #sectionNumber do
            table.remove(sectionNumber)
        end
        while currentLevel > #sectionNumber do
            table.insert(sectionNumber, 0)
        end
        sectionNumber[currentLevel] = sectionNumber[currentLevel] + 1
        return table.concat(sectionNumber, '.')
    end
end
local genSectionNumber = makeGenSectionNumber()
addUnitTest(function()
    local gen = makeGenSectionNumber()
    assert(gen(1) == '1')
    assert(gen(1) == '2')
    assert(gen(2) == '2.1')
    assert(gen(4) == '2.1.0.1')
    assert(gen(3) == '2.1.1')
    assert(gen(1) == '3')
    assert(gen(4) == '3.0.0.1')
    assert(gen(4) == '3.0.0.2')
    assert(gen(2) == '3.1')
    assert(gen(4) == '3.1.0.1')
    assert(gen(1) == '4')

    local gen = makeGenSectionNumber()
    assert(gen(3) == '0.0.1')
    assert(gen(2) == '0.1')
    assert(gen(1) == '1')
end)

local function nextBijectiveAlpha(num)
    local s, e = num:find('[a-y]z*$')
    if not s then
        return ('a'):rep(#num + 1)
    else
        return num:sub(1, s-1) .. string.char(num:byte(s) + 1) .. ('a'):rep(e-s)
    end
end
addUnitTest(function()
    assert(nextBijectiveAlpha('') == 'a')
    assert(nextBijectiveAlpha('a') == 'b')
    assert(nextBijectiveAlpha('b') == 'c')
    assert(nextBijectiveAlpha('y') == 'z')
    assert(nextBijectiveAlpha('z') == 'aa')
    assert(nextBijectiveAlpha('aa') == 'ab')
    assert(nextBijectiveAlpha('az') == 'ba')
    assert(nextBijectiveAlpha('xq') == 'xr')
    assert(nextBijectiveAlpha('zz') == 'aaa')
    assert(nextBijectiveAlpha('fuzz') == 'fvaa')
    assert(nextBijectiveAlpha('gorilla') == 'gorillb')
    assert(nextBijectiveAlpha('zzzzzzz') == 'aaaaaaaa')
end)

--------------------------------------------------------------------------------

-- Table to store footnotes, so they can be included at the end.
local notes = {}
local noteSuffix = ''
local function flushNotes(buffer)
    if #notes > 0 then
        table.insert(buffer, '<section class="footnotes"><hr />')
        for _, note in pairs(notes) do
            table.insert(buffer, note)
        end
        table.insert(buffer, '</section>')
        notes = {}

        -- note numbers are reset, but the link targets should be unique.
        noteSuffix = nextBijectiveAlpha(noteSuffix)
    end
end

-- This function is called once for the whole document. Parameters:
-- body is a string, metadata is a table, variables is a table.
-- This gives you a fragment.  You could use the metadata table to
-- fill variables in a custom lua template.  Or, pass `--template=...`
-- to pandoc, and pandoc will add do the template processing as
-- usual.
function Doc(body, metadata, variables)
    local buffer = {body}
    flushNotes(buffer)
    genSectionNumber = makeGenSectionNumber()
    return table.concat(buffer, '\n')
end

-- Blocksep is used to separate block elements.
function Blocksep()
    return '\n'
end

-- The functions that follow render corresponding pandoc elements.
-- s is always a string, attr is always a table of attributes, and
-- items is always an array of strings (the items in a list).
-- Comments indicate the types of other variables.

function Str(s)
    return s:escape()
end

function Space()
    return ' '
end

function SoftBreak()
    return '\n'
end

function LineBreak()
    return E.br()
end

function Emph(s)
    return E.em(s)
end

function Strong(s)
    return E.strong(s)
end

function Subscript(s)
    return E.sub(s)
end

function Superscript(s)
    return E.sup(s)
end

function SmallCaps(s)
    return E.span{class='small-caps'}(s)
end

function Strikeout(s)
    return E.s(s)
end

function SingleQuoted(s)
    return '‘' .. s .. '’'
end

function DoubleQuoted(s)
    return '“' .. s .. '”'
end

function Link(s, src, tit, attrs)
    return E.a{attrs; href=src, title=tit}(s)
end

function Image(s, src, tit, attrs)
    return E.img{attrs; src=src, alt=s, title=tit}()
end

function CaptionedImage(src, tit, caption, attrs)
    if tit:sub(1, 4) == 'fig:' then tit = tit:sub(5) end
    return E.figure(E.img{attrs; src=src, title=tit}() .. E.figcaption(caption))
end

function Code(s, attrs)
    return E.code{attrs}(s:escape())
end

function InlineMath(s)
    return E.span{class='math math-inline'}(s:escape())
end

function DisplayMath(s)
    return E.span{class='math math-display'}(s:escape())
end

function Note(s)
    local num = #notes + 1
    local id = num .. noteSuffix
    s = s:gsub('(.*)</', '%1 ' .. E.a{class='footnote-back', href='#fnref'..id}('▲') .. '</')
    table.insert(notes, E.section{id='fn'..id}(E.h6(num) .. s))
    return E.a{class='footnote', id='fnref'..id, href='#fn'..id}(
        E.sup(E.span('[') .. num .. E.span(']')))
end

function Span(s, attrs)
    return E.span{attrs}(s)
end

function Cite(s, cs)
    local ids = {}
    for _, cit in ipairs(cs) do
        table.insert(ids, cit.citationId)
    end
    return E.span{class='cite', ['data-citation-ids']=table.concat(ids, ',')}(s)
end

function RawInline(fmt, s)
    if fmt == 'html' then
        return s
    else
        return ''
    end
end

local seenMore = false
function RawBlock(fmt, s)
    if fmt == 'html' then
        if s:match('^<!%-%-%s*notes%s*%-%->$') then
            local buffer = {}
            flushNotes(buffer)
            return table.concat(buffer, '\n')
        elseif s:match('^<!%-%-%s*more%s*%-%->$') and not seenMore then
            seenMore = true
            return E.a{name='more'}(s)
        else
            return s
        end
    else
        return ''
    end
end

function Plain(s)
    return s
end

function Para(s)
    return E.p(s)
end

-- the section number starts with H2, with H1 being ignored.
-- Pandoc somehow confuses the meaning of --base-header-level (unfortunately),
-- so we need to resort on the surgery at the preprocessor or writer level.
function Header(level, s, attrs)
    local htmlLevel = math.min(level + 1, 6)
    if htmlLevel < 6 and not hasClass(attrs, 'unnumbered') then
        local sectionNumber = genSectionNumber(level)
        s = E.span{class='header-section-number'}(sectionNumber) .. ' ' .. s
    end
    return E['h'..htmlLevel]{attrs}(s)
end

function BlockQuote(s)
    return E.blockquote(s)
end

function HorizontalRule()
    return E.hr()
end

function CodeBlock(s, attrs)
    -- If code block has class 'dot', pipe the contents through dot
    -- and base64, and include the base64-encoded png as a data: URL.
    --if hasClass(attrs, 'dot') then
    --    local png = pipe("base64", pipe("dot -Tpng", s))
    --    return '<img src="data:image/png;base64,' .. png .. '"/>'
    --    -- otherwise treat as code (one could pipe through a highlighter)
    --else
    return E.pre(E.code{attrs}(s:escape()))
    --end
end

function BulletList(items)
    local buffer = {''}
    for _, item in pairs(items) do
        table.insert(buffer, E.li(item))
    end
    table.insert(buffer, '')
    return E.ul(table.concat(buffer, '\n'))
end

function OrderedList(items)
    local buffer = {''}
    for _, item in pairs(items) do
        table.insert(buffer, E.li(item))
    end
    table.insert(buffer, '')
    return E.ol(table.concat(buffer, '\n'))
end

-- Revisit association list STackValue instance.
function DefinitionList(items)
    local buffer = {''}
    for _, item in pairs(items) do
        for dt, dds in pairs(item) do
            table.insert(buffer, E.dt(dt))
            for _, dd in ipairs(dds) do
                table.insert(buffer, E.dd(dd))
            end
        end
    end
    table.insert(buffer, '')
    return E.dl(table.concat(buffer, '\n'))
end

-- Convert pandoc alignment to something HTML can use.
-- align is AlignLeft, AlignRight, AlignCenter, or AlignDefault.
function html_align(align)
    if align == 'AlignLeft' then
        return 'left'
    elseif align == 'AlignRight' then
        return 'right'
    elseif align == 'AlignCenter' then
        return 'center'
    else
        return 'left'
    end
end

-- Caption is a string, aligns is an array of strings,
-- widths is an array of floats, headers is an array of
-- strings, rows is an array of arrays of strings.
function Table(caption, aligns, widths, headers, rows)
    local buffer = {}
    local function add(s)
        table.insert(buffer, s)
    end
    add("<table>")
    if caption ~= "" then
        add("<caption>" .. caption .. "</caption>")
    end
    if widths and widths[1] ~= 0 then
        for _, w in pairs(widths) do
            add('<col width="' .. string.format("%d%%", w * 100) .. '" />')
        end
    end
    local header_row = {}
    local empty_header = true
    for i, h in pairs(headers) do
        local align = html_align(aligns[i])
        table.insert(header_row,'<th align="' .. align .. '">' .. h .. '</th>')
        empty_header = empty_header and h == ""
    end
    if empty_header then
        head = ""
    else
        add('<tr class="header">')
        for _,h in pairs(header_row) do
            add(h)
        end
        add('</tr>')
    end
    local class = "even"
    for _, row in pairs(rows) do
        class = (class == "even" and "odd") or "even"
        add('<tr class="' .. class .. '">')
        for i,c in pairs(row) do
            add('<td align="' .. html_align(aligns[i]) .. '">' .. c .. '</td>')
        end
        add('</tr>')
    end
    add('</table>')
    return table.concat(buffer,'\n')
end

function Div(s, attrs)
    return E.div{attrs}(s)
end

--------------------------------------------------------------------------------

-- The following code will produce runtime warnings when you haven't defined
-- all of the functions you need for the custom writer, so it's useful
-- to include when you're working on a writer.
local meta = {}
meta.__index =
    function(_, key)
        io.stderr:write(string.format("WARNING: Undefined function '%s'\n",key))
        return function() return "" end
    end
setmetatable(_G, meta)

if unitTests then
    print('running unit tests...')
    for _, f in ipairs(unitTests) do f() end
    print('done.')
end

-- vim: set ts=4 sts=4 sw=4 et:
