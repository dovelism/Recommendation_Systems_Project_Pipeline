package com.bo.bonews.i;


public interface ItemDragListener {
    void onItemMove(int fromPosition, int toPosition);

    void onItemSwiped(int position);
}
