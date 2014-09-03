=begin
** Form generated from reading ui file 'IspellDictDlg.ui'
**
** Created: Mon Oct 21 01:35:32 2013
**      by: Qt User Interface Compiler version 4.8.5
**
** WARNING! All changes made in this file will be lost when recompiling ui file!
=end

class Ui_IspellDictDlg
    attr_reader :gridLayout_3
    attr_reader :verticalLayout
    attr_reader :lblInputCount
    attr_reader :lstInput
    attr_reader :gridLayout
    attr_reader :lblAddedCount
    attr_reader :btnDefinition
    attr_reader :btnExtendOutput
    attr_reader :btnCut
    attr_reader :btnAdd
    attr_reader :lstDicts
    attr_reader :btnStardict
    attr_reader :btnFindSimilar
    attr_reader :btnAllFlags
    attr_reader :gridLayout_2
    attr_reader :btnSave
    attr_reader :textLabel1_2_2
    attr_reader :lstOutput
    attr_reader :btnRemoveWord
    attr_reader :horizontalSpacer
    attr_reader :txtResult
    attr_reader :txtExtra
    attr_reader :textLabel1_2
    attr_reader :textLabel1_3
    attr_reader :lstSuggestions
    attr_reader :lstDeclinations
    attr_reader :lstKrym

    def setupUi(ispellDictDlg)
    if ispellDictDlg.objectName.nil?
        ispellDictDlg.objectName = "ispellDictDlg"
    end
    ispellDictDlg.resize(742, 564)
    @gridLayout_3 = Qt::GridLayout.new(ispellDictDlg)
    @gridLayout_3.spacing = 6
    @gridLayout_3.margin = 11
    @gridLayout_3.objectName = "gridLayout_3"
    @verticalLayout = Qt::VBoxLayout.new()
    @verticalLayout.spacing = 6
    @verticalLayout.objectName = "verticalLayout"
    @lblInputCount = Qt::Label.new(ispellDictDlg)
    @lblInputCount.objectName = "lblInputCount"
    @lblInputCount.wordWrap = false

    @verticalLayout.addWidget(@lblInputCount)

    @lstInput = Qt::ListWidget.new(ispellDictDlg)
    @lstInput.objectName = "lstInput"
    @sizePolicy = Qt::SizePolicy.new(Qt::SizePolicy::Preferred, Qt::SizePolicy::Expanding)
    @sizePolicy.setHorizontalStretch(0)
    @sizePolicy.setVerticalStretch(0)
    @sizePolicy.heightForWidth = @lstInput.sizePolicy.hasHeightForWidth
    @lstInput.sizePolicy = @sizePolicy
    @lstInput.minimumSize = Qt::Size.new(200, 0)

    @verticalLayout.addWidget(@lstInput)


    @gridLayout_3.addLayout(@verticalLayout, 0, 0, 1, 2)

    @gridLayout = Qt::GridLayout.new()
    @gridLayout.spacing = 6
    @gridLayout.objectName = "gridLayout"
    @lblAddedCount = Qt::Label.new(ispellDictDlg)
    @lblAddedCount.objectName = "lblAddedCount"
    @lblAddedCount.wordWrap = false

    @gridLayout.addWidget(@lblAddedCount, 0, 0, 1, 2)

    @btnDefinition = Qt::PushButton.new(ispellDictDlg)
    @btnDefinition.objectName = "btnDefinition"
    @btnDefinition.enabled = false

    @gridLayout.addWidget(@btnDefinition, 2, 0, 1, 1)

    @btnExtendOutput = Qt::PushButton.new(ispellDictDlg)
    @btnExtendOutput.objectName = "btnExtendOutput"
    @btnExtendOutput.enabled = false

    @gridLayout.addWidget(@btnExtendOutput, 3, 1, 1, 1)

    @btnCut = Qt::PushButton.new(ispellDictDlg)
    @btnCut.objectName = "btnCut"
    @btnCut.enabled = false

    @gridLayout.addWidget(@btnCut, 4, 1, 1, 1)

    @btnAdd = Qt::PushButton.new(ispellDictDlg)
    @btnAdd.objectName = "btnAdd"
    @btnAdd.enabled = false

    @gridLayout.addWidget(@btnAdd, 5, 0, 1, 2)

    @lstDicts = Qt::ListWidget.new(ispellDictDlg)
    @lstDicts.objectName = "lstDicts"

    @gridLayout.addWidget(@lstDicts, 1, 0, 1, 2)

    @btnStardict = Qt::PushButton.new(ispellDictDlg)
    @btnStardict.objectName = "btnStardict"
    @btnStardict.enabled = false

    @gridLayout.addWidget(@btnStardict, 2, 1, 1, 1)

    @btnFindSimilar = Qt::PushButton.new(ispellDictDlg)
    @btnFindSimilar.objectName = "btnFindSimilar"
    @btnFindSimilar.enabled = false

    @gridLayout.addWidget(@btnFindSimilar, 3, 0, 1, 1)

    @btnAllFlags = Qt::PushButton.new(ispellDictDlg)
    @btnAllFlags.objectName = "btnAllFlags"

    @gridLayout.addWidget(@btnAllFlags, 4, 0, 1, 1)


    @gridLayout_3.addLayout(@gridLayout, 0, 2, 1, 1)

    @gridLayout_2 = Qt::GridLayout.new()
    @gridLayout_2.spacing = 6
    @gridLayout_2.objectName = "gridLayout_2"
    @btnSave = Qt::PushButton.new(ispellDictDlg)
    @btnSave.objectName = "btnSave"
    @btnSave.enabled = false

    @gridLayout_2.addWidget(@btnSave, 0, 0, 1, 1)

    @textLabel1_2_2 = Qt::Label.new(ispellDictDlg)
    @textLabel1_2_2.objectName = "textLabel1_2_2"
    @textLabel1_2_2.wordWrap = false

    @gridLayout_2.addWidget(@textLabel1_2_2, 1, 0, 1, 1)

    @lstOutput = Qt::ListWidget.new(ispellDictDlg)
    @lstOutput.objectName = "lstOutput"
    @lstOutput.minimumSize = Qt::Size.new(200, 180)

    @gridLayout_2.addWidget(@lstOutput, 2, 0, 1, 1)


    @gridLayout_3.addLayout(@gridLayout_2, 0, 3, 1, 1)

    @btnRemoveWord = Qt::PushButton.new(ispellDictDlg)
    @btnRemoveWord.objectName = "btnRemoveWord"

    @gridLayout_3.addWidget(@btnRemoveWord, 1, 0, 1, 1)

    @horizontalSpacer = Qt::SpacerItem.new(93, 20, Qt::SizePolicy::Expanding, Qt::SizePolicy::Minimum)

    @gridLayout_3.addItem(@horizontalSpacer, 1, 1, 1, 1)

    @txtResult = Qt::LineEdit.new(ispellDictDlg)
    @txtResult.objectName = "txtResult"
    @txtResult.minimumSize = Qt::Size.new(240, 0)

    @gridLayout_3.addWidget(@txtResult, 1, 2, 1, 1)

    @txtExtra = Qt::LineEdit.new(ispellDictDlg)
    @txtExtra.objectName = "txtExtra"

    @gridLayout_3.addWidget(@txtExtra, 1, 3, 1, 1)

    @textLabel1_2 = Qt::Label.new(ispellDictDlg)
    @textLabel1_2.objectName = "textLabel1_2"
    @textLabel1_2.wordWrap = false

    @gridLayout_3.addWidget(@textLabel1_2, 2, 0, 1, 1)

    @textLabel1_3 = Qt::Label.new(ispellDictDlg)
    @textLabel1_3.objectName = "textLabel1_3"
    @textLabel1_3.wordWrap = false

    @gridLayout_3.addWidget(@textLabel1_3, 2, 2, 1, 1)

    @lstSuggestions = Qt::ListWidget.new(ispellDictDlg)
    @lstSuggestions.objectName = "lstSuggestions"
    @sizePolicy.heightForWidth = @lstSuggestions.sizePolicy.hasHeightForWidth
    @lstSuggestions.sizePolicy = @sizePolicy

    @gridLayout_3.addWidget(@lstSuggestions, 3, 0, 1, 2)

    @lstDeclinations = Qt::ListWidget.new(ispellDictDlg)
    @lstDeclinations.objectName = "lstDeclinations"
    @lstDeclinations.frameShape = Qt::Frame::Panel
    @lstDeclinations.frameShadow = Qt::Frame::Sunken
    @lstDeclinations.selectionMode = Qt::AbstractItemView::NoSelection
    @lstDeclinations.layoutMode = Qt::ListView::Batched

    @gridLayout_3.addWidget(@lstDeclinations, 3, 2, 1, 1)

    @lstKrym = Qt::ListWidget.new(ispellDictDlg)
    @lstKrym.objectName = "lstKrym"

    @gridLayout_3.addWidget(@lstKrym, 3, 3, 1, 1)


    retranslateUi(ispellDictDlg)
    Qt::Object.connect(@btnAdd, SIGNAL('clicked()'), ispellDictDlg, SLOT('addWord()'))
    Qt::Object.connect(@btnCut, SIGNAL('clicked()'), ispellDictDlg, SLOT('getWordBack()'))
    Qt::Object.connect(@btnDefinition, SIGNAL('clicked()'), ispellDictDlg, SLOT('showDefinition()'))
    Qt::Object.connect(@btnExtendOutput, SIGNAL('clicked()'), ispellDictDlg, SLOT('extendWordFlags()'))
    Qt::Object.connect(@btnFindSimilar, SIGNAL('clicked()'), ispellDictDlg, SLOT('findSimilar()'))
    Qt::Object.connect(@btnRemoveWord, SIGNAL('clicked()'), ispellDictDlg, SLOT('removeWord()'))
    Qt::Object.connect(@btnSave, SIGNAL('clicked()'), ispellDictDlg, SLOT('save()'))
    Qt::Object.connect(@btnStardict, SIGNAL('clicked()'), ispellDictDlg, SLOT('getStardict()'))
    Qt::Object.connect(@lstOutput, SIGNAL('currentRowChanged(int)'), ispellDictDlg, SLOT('outputSelected()'))
    Qt::Object.connect(@lstSuggestions, SIGNAL('currentRowChanged(int)'), ispellDictDlg, SLOT('suggSelected()'))
    Qt::Object.connect(@lstSuggestions, SIGNAL('itemDoubleClicked(QListWidgetItem*)'), ispellDictDlg, SLOT('addSuggestedWord()'))
    Qt::Object.connect(@txtResult, SIGNAL('textChanged(QString)'), ispellDictDlg, SLOT('rawTextEdited()'))
    Qt::Object.connect(@lstDicts, SIGNAL('currentItemChanged(QListWidgetItem*,QListWidgetItem*)'), ispellDictDlg, SLOT('dictChanged(QListWidgetItem*,QListWidgetItem*)'))
    Qt::Object.connect(@txtExtra, SIGNAL('textChanged(QString)'), ispellDictDlg, SLOT('extraTextChanged()'))

    Qt::MetaObject.connectSlotsByName(ispellDictDlg)
    end # setupUi

    def setup_ui(ispellDictDlg)
        setupUi(ispellDictDlg)
    end

    def retranslateUi(ispellDictDlg)
    ispellDictDlg.windowTitle = Qt::Application.translate("IspellDictDlg", "\320\240\320\265\320\264\320\260\320\272\321\202\320\276\321\200 \321\201\320\273\320\276\320\262\320\275\320\270\320\272\320\260 aspell", nil, Qt::Application::UnicodeUTF8)
    @lblInputCount.text = Qt::Application.translate("IspellDictDlg", "\320\232\321\226\320\273\321\214\320\272\321\226\321\201\321\202\321\214 \320\262\321\205\321\226\320\264\320\275\320\270\321\205 \321\201\320\273\321\226\320\262: 0", nil, Qt::Application::UnicodeUTF8)
    @lblAddedCount.text = Qt::Application.translate("IspellDictDlg", "\320\224\320\276\320\264\320\260\320\275\320\276: 0, \320\262\320\270\320\273\321\203\321\207\320\265\320\275\320\276: 0, \320\267\320\274\321\226\320\275\320\265\320\275\320\276: 0", nil, Qt::Application::UnicodeUTF8)
    @btnDefinition.text = Qt::Application.translate("IspellDictDlg", "&r2u.org.ua", nil, Qt::Application::UnicodeUTF8)
    @btnDefinition.shortcut = Qt::Application.translate("IspellDictDlg", "Alt+\320\222", nil, Qt::Application::UnicodeUTF8)
    @btnExtendOutput.toolTip = Qt::Application.translate("IspellDictDlg", "Returns word back to the input", nil, Qt::Application::UnicodeUTF8)
    @btnExtendOutput.text = Qt::Application.translate("IspellDictDlg", "\320\240\320\276\320\267\321\210\320\270\321\200\320\270\321\202\320\270", nil, Qt::Application::UnicodeUTF8)
    @btnExtendOutput.shortcut = ''
    @btnCut.toolTip = Qt::Application.translate("IspellDictDlg", "Returns word back to the input", nil, Qt::Application::UnicodeUTF8)
    @btnCut.text = Qt::Application.translate("IspellDictDlg", "<< \320\222\320\270\320\264\321\200\320\260\321\202\320\270", nil, Qt::Application::UnicodeUTF8)
    @btnAdd.text = Qt::Application.translate("IspellDictDlg", "\320\224\320\276\320\264&\320\260\321\202\320\270 >>", nil, Qt::Application::UnicodeUTF8)
    @btnAdd.shortcut = Qt::Application.translate("IspellDictDlg", "Alt+\320\220", nil, Qt::Application::UnicodeUTF8)
    @btnStardict.text = Qt::Application.translate("IspellDictDlg", "Stardict (&\321\201)", nil, Qt::Application::UnicodeUTF8)
    @btnStardict.shortcut = Qt::Application.translate("IspellDictDlg", "Alt+\320\241", nil, Qt::Application::UnicodeUTF8)
    @btnFindSimilar.toolTip = Qt::Application.translate("IspellDictDlg", "Returns word back to the input", nil, Qt::Application::UnicodeUTF8)
    @btnFindSimilar.text = Qt::Application.translate("IspellDictDlg", "\320\227\320\275\320\260\320\271\321\202\320\270 \321\201\321\205\320\276\320\266\321\226", nil, Qt::Application::UnicodeUTF8)
    @btnFindSimilar.shortcut = ''
    @btnAllFlags.text = Qt::Application.translate("IspellDictDlg", "\320\237\320\276\320\262\320\275\320\270\320\271 \320\275\320\260\320\261\321\226\321\200", nil, Qt::Application::UnicodeUTF8)
    @btnSave.text = Qt::Application.translate("IspellDictDlg", "\320\227\320\261\320\265\321\200\320\265\320\263\321\202\320\270", nil, Qt::Application::UnicodeUTF8)
    @textLabel1_2_2.text = Qt::Application.translate("IspellDictDlg", "\320\241\321\205\320\276\320\266\321\226 \320\275\320\260\321\217\320\262\320\275\321\226 \321\201\320\273\320\276\320\262\320\260:", nil, Qt::Application::UnicodeUTF8)
    @btnRemoveWord.toolTip = Qt::Application.translate("IspellDictDlg", "Removes the input word", nil, Qt::Application::UnicodeUTF8)
    @btnRemoveWord.text = Qt::Application.translate("IspellDictDlg", "\320\222\320\270\320\273\321\203\321\207\320\270\321\202\320\270", nil, Qt::Application::UnicodeUTF8)
    @textLabel1_2.text = Qt::Application.translate("IspellDictDlg", "\320\237\321\200\320\276\320\277\320\276\320\267\320\270\321\206\321\226\321\227 \320\262\321\226\320\264 aspell:", nil, Qt::Application::UnicodeUTF8)
    @textLabel1_3.text = Qt::Application.translate("IspellDictDlg", "\320\241\320\273\320\276\320\262\320\276\321\204\320\276\321\200\320\274\320\270:", nil, Qt::Application::UnicodeUTF8)
    @lstDeclinations.toolTip = Qt::Application.translate("IspellDictDlg", "\320\227\320\263\320\265\320\275\320\265\321\200\320\276\320\262\320\260\320\275\321\226 \321\201\320\273\320\276\320\262\320\276\321\204\320\276\321\200\320\274\320\270", nil, Qt::Application::UnicodeUTF8)
    end # retranslateUi

    def retranslate_ui(ispellDictDlg)
        retranslateUi(ispellDictDlg)
    end

end

module Ui
    class IspellDictDlg < Ui_IspellDictDlg
    end
end  # module Ui

