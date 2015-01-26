#!/usr/bin/ruby
# encoding: utf-8

#$KCODE      = 'UTF-8'


require 'Qt'
require 'uri'

require './ui/IspellDictDlg'


require './aspell-helper'
require './aspell-stats'
require './asp-util'


$aspellSuggestions = true

class MyDlg < Qt::Widget
	TAB_NOUN = 0
	TAB_VERB = 1
	TAB_ADJ = 2

    def initialize(parent = nil)
        super
#	  super(parent, name, fl)

        @d = Ui_IspellDictDlg.new()
        height = Qt::DesktopWidget.new().availableGeometry().height
        @d.setupUi(self)
#        d.setupUi(self)
        resize(-1, height)

	  @stats = Stats.new
	  @origWordMap = Hash.new(0)


	  @wordsHandled = 0
	  @wordsAdded = 0
	  @wordsRemoved = 0
	  @wordsChanged = 0

	  @deletingInput = false

    end


    slots 'languageChange()',
    'addWord()',
    'addSuggestedWord()',
    'removeWord()',
    'duplicateWord()',
    'getStardict()',
    'getWordBack()',
#    'dictChanged()',
    'notDeclined()',
    'rawTextEdited()',
    'save()',
    'suggSelected()',
    'wordSelected()',
    'outputSelected()',
    'showDefinition()',
	'save()',
	'extendWordFlags()',
	'findSimilar()',
	'dictChanged(QListWidgetItem*,QListWidgetItem*)',
	'extraTextChanged()'

  def update_counters
	@d.lblInputCount.setText("Вхідних слів: #{SrcList.count.to_s} (обр. #{@wordsHandled})")
	@d.lblAddedCount.setText("Додано: #{@wordsAdded}, вилучено: #{@wordsRemoved}, змінено: #{@wordsChanged}")
	canSave = (@wordsHandled + @wordsAdded + @wordsRemoved + @wordsChanged > 0)
	@d.btnSave.setEnabled(canSave)
  end

  def save()
	save_changes
	@wordsHandled = 0
	@wordsAdded = 0
	@wordsRemoved = 0
	@wordsChanged = 0
	update_counters
  end

  def extendWordFlags
        return if @d.lstOutput.currentItem == nil
  
	txt2 = @d.lstOutput.currentItem.text.force_encoding('utf-8')
	
	return if txt2 == nil
	
	ot = txt2.delete(' ').split(/:/)
	dict = ot[0]
	oldStr = ot[1]

	resultText = @d.txtResult.text.force_encoding('utf-8')
	newFlags = get_flags( resultText )

	if oldStr.include?('/')
	  oldFlags = get_flags( oldStr )

	  resultFlags = (oldFlags + newFlags).squeeze

	  newTxt = oldStr.split('/')[0] + '/' + resultFlags
	else
	  newTxt = oldStr + '/' + newFlags
	end
	
	declinedItems = getDeclinedWords()

	add_word_to_dict(dict, newTxt)
	remove_word_from_dict(dict, oldStr)
	@wordsChanged += 1
	
	cnt = remove_derivatives_from_input(newTxt, declinedItems)
	@wordsHandled += cnt
	
	update_counters
  end

  def showDefinition()
	txt = @d.txtResult.text
	txt = txt.split('/')[0] if txt.include?('/')

#	txtEnc = URI.escape("http://www.slovnyk.net/?swrd=#{txt}")
#	txtEnc = "http://www.slovnyk.net/?swrd=#{txt}".gsub( /'/, "%27" ) #'
	txt = txt.gsub( /'/, "%27" ) #'
	txtEnc = "'http://r2u.org.ua/krym/krym_search.php?word_str=#{txt}&type=ukrq&highlight=on'";
#	runCmd = "dcop `dcop konq* | head -1` konqueror-mainwindow#1 #{txtEnc}"
#	runCmd = "dcop `dcop konq* | head -1` default createNewWindow #{txtEnc}"
#	runCmd = "dcop klauncher klauncher 'kdeinit_exec(QString,QStringList)' konqueror '(' #{txtEnc} ')'"
#	runCmd = "xdg-open #{txtEnc}"
	runCmd = "firefox #{txtEnc}"
#	puts "konqueror #{txtEnc} 2>/dev/null >/dev/null &"
#	cmd = IO.popen("konqueror \"#{txtEnc}\" &", "r+")
	cmd = IO.popen(runCmd, mode: 'r+:UTF-8')
    cmd.close
  end

  def outputSelected()

	@d.btnCut.setEnabled( @d.lstOutput.currentItem != -1 )

	txt = @d.txtResult.text
	return if txt.empty? or @d.lstOutput.currentItem == -1
	
	t = txt.split('/')
	word = t[0]
	flags = t[1]

        return if @d.lstOutput.currentItem == nil

	outText = @d.lstOutput.currentItem.text
	ot = outText.delete(' ').split(/[:\/]/)

	if word == ot[1] and flags != ot[2]
	  @d.btnExtendOutput.setEnabled(true)
	else
	  @d.btnExtendOutput.setEnabled(false)
	end

#	@d.btnCut.setEnabled(ot[3] != nil)
	
  end


  def setFlags(flags)
	txt = @d.txtResult.text
	return if txt.empty?
	
	if txt.include?("/")
	  txt = /^[^\/A-Za-z]+/.match( txt )[0]
	end
	
	if( ! flags.empty? )
	  txt << "/"
	end
	@d.txtResult.setText( txt << flags )
  end


  def getStardict
	txt = @d.txtResult.text
	txt = txt.split('/')[0] if txt.include?('/')

#	txtEnc = "#{txt}".gsub( /'/, '\\'' )	#'
	runCmd = "stardict \"#{txt}\" &"
	cmd = IO.popen(runCmd, mode: 'r+:UTF-8')
    cmd.close
  end
  
  def getDeclinations
        wrd = @d.txtResult.text.force_encoding('utf-8')
	expands = aspell_expand( wrd )
	@d.lstDeclinations.clear
	for ex in expands
		@d.lstDeclinations.addItem(ex)
	end
  end

  def removeWord(*k)
	return if ! @d.lstInput.currentIndex.isValid
  
        currentRow = @d.lstInput.currentIndex.row
	nextItem = currentRow < SrcList.count-1 ? currentRow : currentRow - 1
	
	txt = @d.lstInput.currentItem.text.force_encoding('utf-8')
	puts "removing #{txt} from source"
	SrcList.delete( txt )
#	@d.lstInput.removeItemWidget( @d.lstInput.currentItem )
	@d.lstInput.takeItem( currentRow )
	@d.lstInput.setCurrentRow( nextItem )
#	@d.lstInput.setCurrentItem( nextItem )
	
	@wordsHandled += 1
	update_counters
	
	wordSelected()
  end

  def getDeclinedWords()
	declinedItems = []
	expandedItems = @d.lstDeclinations.findItems('.*', Qt::MatchRegExp)
	
	for declinedItem in expandedItems
	    declinedItems << declinedItem.text
	end

#	puts "expItems: #{declinedItems}"
	declinedItems
  end


  def addWord(*k)
    begin
	_addWord(k)
    rescue e
	puts "Oops #{e}"
    end
  end
  
  def _addWord(*k)
#	@d.lstOutput.addItem( @d.txtResult.text )
#	@origWordMap[ @d.txtResult.text ] = @d.lstInput.currentItem.text

        txt = @d.txtResult.text.force_encoding('utf-8')
	return if /[5-9]/.match( txt ) 
	dict = @d.lstDicts.currentItem.text.force_encoding('utf-8')
	
	word = txt
	
	extra = @d.txtExtra.text.force_encoding('utf-8')
	if extra != ''
	    txt += ' ' + extra
	end
	
	declinedItems = getDeclinedWords()

	add_word_to_dict( dict, txt )
	@wordsAdded += 1

	cnt = remove_derivatives_from_input( word, declinedItems )
	@wordsHandled += cnt

	@d.txtExtra.text = ''

#	@d.txtResult.clear
#	@d.lstOutput.clear
	
	update_counters
  end

  def addSuggestedWord(*k)
        puts "addSuggestedWord"
	@d.txtResult.setText( @d.lstSuggestions.currentItem.text )
	addWord(k)
  end

  def remove_derivatives_from_input( txt, declinedItems )
	#expands = aspell_expand( txt )
	
	cnt = 0
	@deletingInput = true
	for declinedItem in declinedItems
	    items = @d.lstInput.findItems(declinedItem, Qt::MatchFixedString)
	    items.each do |item|
		puts "removing #{declinedItem} from source"
		SrcList.delete( item.text.force_encoding('utf-8') )
#		@d.lstInput.removeItemWidget( item )
		@d.lstInput.takeItem( @d.lstInput.row(item) )
		cnt += 1
	    end
	end

	currRow = @d.lstInput.currentRow
	@d.lstInput.scrollTo( @d.lstInput.currentIndex() )

#	@d.lstInput.currentRow = 0
#	@d.lstInput.currentRow = currRow
#	@d.lstInput.item( currRow ).setSelected(true)

#	@d.lstInput.scrollTo( @d.lstInput.currentIndex().sibling(-15, 0) )

	@deletingInput = false
	

        wordSelected

#	currItem = @d.lstInput.currentItem
#	if currItem != nil
#	  @d.lstInput.setCurrentItem( currItem )
#	end

	cnt
  end

  def getWordBack(*k)
        item = @d.lstOutput.currentItem
	return if item == nil
	
	outText = item.text.force_encoding('utf-8')
#	ot = outText.delete(' ').split(/[:]/)
	puts "xx1: " +outText
	otx = outText.split(/ : /)
	ot = otx[1].strip().split(' ')
	puts "xx2: " +ot[0] + ", " #+ot[1]
	@d.txtResult.setText( ot[0] )
	@d.txtExtra.setText( ot[1] )
	@d.lstOutput.takeItem( @d.lstOutput.currentRow )

	remove_word_from_dict(otx[0], ot[0])
	@wordsRemoved += 1

	update_counters
  end

  def rawTextEdited()
	text = @d.txtResult.text.force_encoding('utf-8')
	
	noText = text == nil or text == ''
	@d.btnDefinition.setEnabled( !noText )
	@d.btnStardict.setEnabled( !noText )
	
	wellFormed = /^[а-яіїєґ'-]+(\/[a-zA-Z0-9]+(<>?)?\+?-?)?$/i.match(text) ? true : false	#'
	#puts "wellFormed #{wellFormed}"
	@d.btnAdd.setEnabled( wellFormed )
	
	return if noText or not wellFormed

        getDeclinations
	
#	@d.btnDecline.setEnabled(true)
#	@d.btnAdd.setEnabled( text.length > 0 )
	@d.btnDefinition.setEnabled( text.length > 0 )
	@d.btnStardict.setEnabled( text.length > 0 )
	
#	puts get_word(@d.txtResult.text) + "," + get_word(@d.lstSuggestions.currentItem.text)
	changed = (@d.lstSuggestions.currentItem == nil or get_word(text) != get_word(@d.lstSuggestions.currentItem.text))
	@d.btnFindSimilar.setEnabled(changed)
  end

  def suggSelected(*k)
        currItem = @d.lstSuggestions.currentItem
	curText = currItem != nil ? currItem.text.force_encoding('utf-8') : ""

#	puts "=====: #{curText.force_encoding('utf-8')}"
#	puts "текст: #{curText.force_encoding('utf-8')}"
	puts "текст: #{curText}"

	@d.txtResult.setText( "" )
	
	
#	matches = /[A-Za-z]+/.match(curText)

        currItem = @d.lstSuggestions.currentItem
	curText = currItem != nil ? currItem.text.force_encoding('utf-8') : ""
	@d.txtResult.setText( curText )

	matches = /^[^\/]+/.match(curText)
        if matches
            clipboard = Qt::Application::clipboard()
            clipboard.setText(matches[0])
        end

	populate_similar( get_word(curText) )
  end

  def populate_similar(txt)
	@d.lstOutput.clear
	@d.lstKrym.clear
	return if txt.empty?

        txt = txt.force_encoding('utf-8')
        puts "шукаємо схожі для: #{txt}"

	founds = find_in_dicts( txt )
	exactMatchIndex = -1

	for found in founds
	  @d.lstOutput.addItem( "#{found[0]} : #{found[1]}" )

	  if get_word(found[1]) == txt
		exactMatchIndex = @d.lstOutput.count - 1
#		@d.lstOutput.setSelected( @d.lstOutput.count - 1, true )
	  end
	end
	@d.lstOutput.setCurrentRow( exactMatchIndex )
	
	krym_lst = find_in_krym( txt )
	for found in krym_lst
	  @d.lstKrym.addItem( "#{found}" )
	end
  end

  def findSimilar(*k)
	curText = @d.txtResult.text
	populate_similar( get_word(curText) )
  end

  def wordSelected(*k)
	return if @deletingInput
  
	str = SrcList[ @d.lstInput.currentIndex.row ]
	return if str == nil
	
        puts "вибране слово: #{str}"
	@d.txtResult.setText('')

	suggestions = @stats.suggestions_by_suffix(str)

	@d.lstSuggestions.clear
	@d.lstSuggestions.addItem(str)

	if suggestions != 0
	  first = true
	  for sugg in suggestions
		if sugg != nil
		  @d.lstSuggestions.addItem(str + "/" + sugg[0])
		  if first
			@d.lstSuggestions.setCurrentRow( @d.lstSuggestions.count() - 1 )
			first = false
		  end
		end
	  end
	else
	  suggestions = []
#	  @d.lstSuggestions.setCurrentRow( 0 )
	end
	
	if $aspellSuggestions
	  munches = aspell_munch( str )
	  for munch in munches
		if munch != nil and munch != str && ! suggestions.include?(munch)
#		  puts "ще пропозиція #{munch}"
		  @d.lstSuggestions.addItem( munch )
		end
	  end
	end
	
	if @d.lstSuggestions.currentIndex.row == -1
#	    if @d.lstSuggestions.count() == 1
		@d.lstSuggestions.setCurrentRow(0)
#	    else
#		@d.lstSuggestions.setCurrentRow(1)
#	    end
	end
  end


  def switch_tab(flag)

#	tab = get_tab(flag)
#	return if @flagToBtns[ flag ] == nil

#	for btn in @flagToBtns[ flag ]
#	  btn.setChecked( true ) unless btn == nil
#	end
#
#	wordGroupTag.setCurrentPage(tab) if tab != nil
  end
  
  def get_tab(flag)
    if "abcdefghijklmnp".include?(flag)
	  tab = TAB_NOUN
    end
    if "ABIJKLMNGHCDEF".include?(flag)
	  tab = TAB_VERB
    end
    if "UVWY".include?(flag)
	  tab = TAB_ADJ
	end
	
	tab
  end

  def fill_dialog()
#        model = Qt::StringListModel.new(SrcList)
#        @d.lstInput.setModel(model)
  
  
Qt::Object.connect(@d.lstInput, SIGNAL('currentRowChanged(int)'), self, SLOT('wordSelected()'))

	for item in SrcList
	  @d.lstInput.addItem( item );
	end

	for item in DictList
	 # if "base-abbr.lst" && item != "pronouns.lst"
	  if item != "pronouns.lst" and item != 'tag.lst' and item != 'lang.lst'
		@d.lstDicts.addItem( item );
		if item == "base.lst"
		  @d.lstDicts.setCurrentRow( @d.lstDicts.count - 1 )
		end
	  end
	end
  end

  def dictChanged(*k, l)
	dict = @d.lstDicts.currentItem.text.force_encoding('utf-8')
	color = dict == 'base.lst' ? 'white' : dict == 'twisters.lst' ? 'pink' : 'yellow'
	@d.txtResult.setStyleSheet( 'background: ' + color )
  end
  
  def extraTextChanged()
	text = @d.txtExtra.text.force_encoding('utf-8')
	if /[,;] |́/.match(text)
	    text.sub!(/[,;] /, '|')
	    text.sub!(/́/, '')
	    @d.txtExtra.text = text
	end
  end

  def closeEvent( event )

	if @wordsHandled > 0 || @wordsAdded > 0 || @wordsRemoved > 0 || @wordsChanged > 0

	  if Qt::MessageBox.warning(self, "Підтвердження виходу", "Існують незбережені зміни! Що будемо робити?", "Повернутися", "Вийти") != 1
		return	  
	  end
		
	end

	event.accept()
  end

end

def split(str)
  if str.include?('/')
	str.split('/')
  else
	[ str, '' ]
  end
end

def split3(str)
  if str.include?('/')
	str.split('/') << '/'
  else
	[ str, '', '' ]
  end
end

def get_word(str)
  split(str)[0]
end

def get_flags(str)
  split(str)[1]
end


inputFile = nil

if ARGV.length >= 2 and ARGV[0] == '-f'
  inputFile = ARGV[1]
  if ! File.exist?(inputFile)
	exit 1
  end
end
puts "source file #{inputFile}"

if ARGV.length >= 3 and ARGV[2] == '-nas'
  $aspellSuggestions = false
end


load_source_list(inputFile)

a = Qt::Application.new(ARGV)
w = MyDlg.new()


w.fill_dialog
w.update_counters

#a.mainWidget = w
w.show()
a.exec()
