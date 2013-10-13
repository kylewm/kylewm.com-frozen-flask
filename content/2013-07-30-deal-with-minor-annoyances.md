---
category = "Programming"
layout = "post"
tags = [ "java", "swing", "documentation",]
abstract = "What to do when you can't bear the thought of writing the same GUI code for the nine thousandth time"
title = "Represent common Swing behaviors as UIConditions"
date = 2013-07-30T00:00:00Z
slug = "deal-with-minor-annoyances"
---

I still do a lot of work with Java Swing (am I the only one?). When
reviewing my own or someone else's additions, it's pretty easy to tell
how much time and attention the person was willing to devote to any
given UI component. For example take a dialog box with a list box, up
and down arrows for re-ordering the things in the list, and a few
buttons on the bottom (Add, Remove, OK). Here are some sample
considerations:

 * The user should be allowed to multi-select items in the list box.
 * If multiple items are selected, reordering or removing better
   affect all items, not just the lead selection.
 * Adding a new item should select the new item and scroll to it.
 * The remove and reorder buttons should only be enabled if one or
   more items is selected.
 * If the dialog was resized the last time it was open, it might be
   nice for it to retain that new size.
 * The escape key should dismiss the dialog.

These sorts of things make all the difference in how polished and
professional an application feels, but when you work on a lot of
prototype-y software, you don't have a lot of time for polishing. Plus
it's a royal pain to have to wire up all these things every single
time.

One option is to create a ReorderableListPanel that will abstract out
some of these considerations so you don't have to keep writing them
over and over. But what about when it's a JTable instead of a JList?
Now I need a ReorderableTablePanel; should they share a common
ancestor? ReorderableThingPanel? I think it's clear that this is too
high a level of abstraction, and we need to dig into the guts a little
and look for a composable solution.

Just as an example, I will try to tackle the button enabledness in a
flexible, reusable, literate way. In the end, I want a one-line
definition whose function is immediately obvious, something like
`button.setEnabled(new ListSelectedCondition(list))`.

Idea: Introduce an abstract UICondition class. A UICondition
represents some changing state (eg, a boolean or String). When the
underlying state changes, the UICondition fires off an event that lets
the component know. Implementations of UIConditions could check for
things like "item(s) in a list are selected" (for Remove) or "*only one*
item in a list is selected" (for Edit). 

Here is a rough sketch of the definition for UICondition:

    :::java
    public abstract class UICondition {

        private List<UIConditionListener> _listeners = new ArrayList<UIConditionListener>();

        private boolean everFired = false;
        private boolean lastFiredCondition = false;

        public abstract boolean isCondition();

        // Implementers should call this whenever the condition may have changed
        protected void maybeConditionChanged() {
            boolean condition = isCondition();
            if (!everFired || lastFiredCondition != condition) {
                fireConditionChanged(condition);
            }
        }	

        private void fireConditionChanged(boolean condition) {
            for (UIConditionListener listener : new ArrayList<UIConditionListener>(_listeners)) {
                listener.conditionChanged(condition);
            }
            everFired = true;
            lastFiredCondition = condition;
        }	

        public void addConditionListner(UIConditionListener listener) {
            _listeners.add(listener);
        }	

        public void removeConditionListener(final UIConditionListener listener) {
            _listeners.remove(listener);
        }	
    }


Notice the `everFired` field which lets us manually trigger the first
event when the condition is first added to a component, even thought
the condition has not yet "changed". Here is a simple implementation
of ListSelectedCondition:

    :::java
    import javax.swing.ListSelectionModel;
    import javax.swing.event.ListSelectionEvent;
    import javax.swing.event.ListSelectionListener;

    public class ListSelectedCondition extends UICondition
        implements ListSelectionListener {

        private ListSelectionModel _model;

        public ListSelectedCondition(ListSelectionModel model) {
            _model = model;
            _model.addListSelectionListener(this);
        }

        public boolean isCondition() {
            return _model.getLeadSelectionIndex() != -1;
        }

        @Override
        public void valueChanged(ListSelectionEvent e) {
            maybeConditionChanged();
        }	
    }

I've become a little bit obsessed with the Builder pattern recently,
and ButtonBuilder gives me a really convenient place to use this
condition:

    :::java
    public ButtonBuilder setEnabled(UICondition condition) {
        _button.setEnabled(condition.isCondition());
        condition.addConditionListner(new UIConditionListener(){
            @Override
            public void conditionChanged(boolean condition) {
                _button.setEnabled(condition);
            }});
        return this;
    }

I can use this guy on any ListSelectionModel (which conveniently is
also used by JTables), I never have to wire up another
ListSelectionListener and more importantly maintainers don't have to
dig through a pile of boilerplate to find the meaningful code. Huzzah!


**Documentation**

This is tangentially related, but whenever you find yourself checking
documentation for the [same thing over and over and over again](http://thecodelesscode.com/case/104), consider:

 * Make the interface self-documenting. Instead of calling something
   "priority" (you will have to check every single time whether
   priority 1 is higher than 2), try "importance" (where a larger
   number always means more important). Instead of returning an
   integer representing minutes, return a Duration.
 * Define a descriptive enumeration rather than an opaque
   boolean/integer. (maybe the thing that has stuck with me the most
   from the great [Effective Java](http://www.powells.com/biblio/9780321356680)).
 * If your interface is too widespread or costly to change, try just
   defining a few constants and use them in the future. Instead of
   returning true, return SUCCESS.