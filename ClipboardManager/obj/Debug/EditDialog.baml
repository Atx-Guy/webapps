   M S B A M L   `   `   `  ����  ClipboardManager!    ClipboardManager.EditDialog   5   	   R NWindowsBase, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35\ XPresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35W SPresentationCore, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35D 9http://schemas.microsoft.com/winfx/2006/xaml/presentation    5   	   R NSystem.Xaml, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     5   	     � Title$  Edit Clipboard Item��5   	    � SizeToContent$ WidthAndHeight=�5   	    � WindowStartupLocation$ CenterScreen=�5   	   ���#F5F5F5.��5      � $��10q�6    � RowDefinitions 5	   
   �� 5      $
��Auto �6   �� 5      $��* �6   �� 5      $
��Auto �6   .+�5   
   �� $��Edit Clipboard Item��6   $��20(�5      $
��Bold"�5      $��Center=�5      $��0,0,0,10q�5      �� 5   
   $
��Auto=�6   $��1��6:   .��5      �� -   5        $��EditTextBox��5       �� TextWrapping$
 Wrap=�5       �� AcceptsReturn . $	��300��5      $��0,0,0,10q�5      $��Stretch=�5       5!      �� 5$   
   -   5        $
��Save��5$      $��2��5%      $��Stretch=�5&      $��Center=�5'      $��40��5(      $��
10,10,10,0q�5)      ��5+      �� 5,       �� 
TargetType" ��6"   .R�5-      �� $��PART_Border��6   ���#007ACC �� CornerRadius$ 5��5/       J� SnapsToDevicePixels . ._�51      �� #��z��6$   $��Center=�52   $   $��Center=�53   $   $
��Bold"�54   $   	 �� Padding$
	 10,5q�55   $   
�������56   $   57      
 �� Triggers
 58      P� 5:       P� Property �@J�IsMouseOver P� Value . . �5;      ��  �� 
TargetName$ PART_Border��6%    �� Property � �� �� Value �#005A9E6T   5<      P� 5>       � �� . . �5?      �� $ PART_Border��6%    � �� �#003F736T   5@      5B      5D      5E      5F      