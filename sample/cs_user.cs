/*
 * このコードは自動生成です。
 * 手動で編集せず、別ファイルにpartial classを定義して拡張してください。
 */
using System;
using System.Collections.Generic;

namespace MasterDataTable
{
    public partial class User
    {
        public int ID;
        public string FamilyName;
        public string FirstName;
        public DateTime Birthday;
        public int _Preference;

        public static User ParseList(List<object> row)
        {
            var obj = new User();
            obj.ID = (int)(long)row[0];
            obj.FamilyName = (string)row[1];
            obj.FirstName = (string)row[2];
            obj.Birthday = DateTime.Parse((string)row[3]);
            obj._Preference = (int)(long)row[4];
            return obj;
        }

        public Preference Preference { get { return MasterData.Preference[this._Preference]; } }
    }
}
