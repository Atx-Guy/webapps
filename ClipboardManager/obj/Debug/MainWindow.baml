   M S B A M L   `   `   `  ����  ClipboardManager!    ClipboardManager.MainWindow   5   	   R NWindowsBase, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35\ XPresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35W SPresentationCore, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35D 9http://schemas.microsoft.com/winfx/2006/xaml/presentation    5   	   R NSystem.Xaml, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     5   	     � Title$  Clipboard Manager��5   	   $	��400��5   	   $	��600��5   	    � WindowStartupLocation$ CenterScreen=�5   	   ���#F5F5F5.��5	      � $��10q�6    � RowDefinitions 5
   
   �� 5      $
��Auto �6   �� 5      $��* �6   �� 5      $
��Auto �6   .+�5   
   �� $��Clipboard Manager��6   $��20(�5      $
��Bold"�5      $��Center=�5      $��0,0,0,10q�5      �� 5   
   -   5        $��ClipboardListBox��5      $��1��5   
   $��0,0,0,10q�5   
   
����������#CCCCCC$��1q�5    
    �� SelectionMode$ Single=�5!   
   ��5"      �� 5#      .R�5$      ��  �� Orientation$ 
Horizontal=�6!   .+�5%      �� $��Center=�65   ��6$   �� 65   5&      5'       � ContextMenu 5+      �� 5,      .@�5-      m� -   5        $
��Edit��5-      6-   m� 5.      -   5        $��Delete��5.      6/   5/      51      �� 55   
   -   5        $��	Clear All��55      $��2��56      $��Stretch=�57      $��Center=�58      $��40��59      $��
10,10,10,0q�5:      ��5<      �� 5=       �� 
TargetType" ��6"   .R�5>      �� $��PART_Border��6   ���#FF5722 �� CornerRadius$ 5��5@       J� SnapsToDevicePixels . ._�5B      �� #��z��6$   $��Center=�5C   $   $��Center=�5D   $   $
��Bold"�5E   $   	 �� Padding$
	 10,5q�5F   $   
�������5G   $   5H      
 �� Triggers
 5I      P� 5K       P� Property �@J�IsMouseOver P� Value . . �5L      ��  �� 
TargetName$ PART_Border��6%    �� Property � �� �� Value �#E64A196T   5M      P� 5O       � �� . . �5P      �� $ PART_Border��6%    � �� �#D843156T   5Q      5S      5U      5V      5W      